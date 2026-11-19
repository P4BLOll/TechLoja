import os
import re
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

from gerar_dados import PRODUTOS, gerar_avaliacoes_antigas, gerar_avaliacoes_novas

# Palavras ignoradas na contagem de causas das reclamacoes
STOPWORDS = {
    "a", "ao", "as", "com", "da", "das", "de", "do", "dos", "e", "em", "é", "mais",
    "mas", "muito", "na", "nas", "não", "no", "nos", "o", "os", "ou", "para", "pelo",
    "por", "porém", "que", "se", "sem", "só", "um", "uma", "fone", "smartwatch",
    "relógio", "caixa", "som", "carregador", "produto", "péssimo", "péssima",
    "horrível", "ruim", "recomendo", "defeito", "funcionar", "primeira", "semana",
    "demais", "rápido", "pouco", "tudo", "todo", "lado", "alta", "alto", "celular",
}


def contar_palavras(textos: pd.Series, top_n: int = 8) -> list[tuple[str, int]]:
    contador = Counter()
    for txt in textos:
        palavras = re.findall(r"[a-záàâãéêíóôõúç]+", str(txt).lower())
        contador.update([p for p in palavras if len(p) > 2 and p not in STOPWORDS])
    return contador.most_common(top_n)


def main():
    os.makedirs("tabelas", exist_ok=True)
    os.makedirs("graficos", exist_ok=True)

    caminho_antigas = "tabelas/avaliacoes_antigas.csv"
    caminho_novas = "tabelas/avaliacoes_novas.csv"
    caminho_classificadas = "tabelas/avaliacoes_novas_classificadas.csv"

    # 1. Carrega ou gera as bases de dados (400 antigas e 150 novas)
    if not os.path.exists(caminho_antigas) or not os.path.exists(caminho_novas):
        df_antigas = gerar_avaliacoes_antigas(400)
        df_novas = gerar_avaliacoes_novas(150)
        df_antigas.to_csv(caminho_antigas, index=False, encoding="utf-8")
        df_novas.to_csv(caminho_novas, index=False, encoding="utf-8")
    else:
        df_antigas = pd.read_csv(caminho_antigas)
        df_novas = pd.read_csv(caminho_novas)

    # 2. Vetorizacao simples (Bag of Words) e Modelo Pequeno (Naive Bayes)
    vetorizador = CountVectorizer()
    X = vetorizador.fit_transform(df_antigas["texto_avaliacao"])
    y = df_antigas["sentimento"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    modelo = MultinomialNB()
    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)
    acuracia = accuracy_score(y_test, y_pred)

    print("=" * 58)
    print("  TREINAMENTO DO MODELO (400 AVALIACOES ANTIGAS)")
    print("=" * 58)
    print("Modelo utilizado: Multinomial Naive Bayes + CountVectorizer")
    print(f"Acuracia no conjunto de teste (80 avaliacoes): {acuracia * 100:.2f}%\n")
    classes = ["Negativa", "Neutra", "Positiva"]
    print(classification_report(y_test, y_pred, target_names=classes))

    # 3. Treina com as 400 avaliacoes antigas e classifica as 150 novas (so texto)
    modelo.fit(X, y)
    X_novas = vetorizador.transform(df_novas["texto_avaliacao"])
    df_novas["sentimento_previsto"] = modelo.predict(X_novas)
    df_novas.to_csv(caminho_classificadas, index=False, encoding="utf-8")

    # 4. Relatorio para o Gerente
    print("=" * 58)
    print("  RELATORIO PARA O GERENTE (150 AVALIACOES NOVAS)")
    print("=" * 58)
    print("\n1) PERCENTUAL DE AVALIACOES POSITIVAS DE CADA PRODUTO:")
    print("-" * 58)

    resumo = []
    for prod in PRODUTOS:
        sub = df_novas[df_novas["produto"] == prod]
        total = len(sub)
        pos = int((sub["sentimento_previsto"] == "Positiva").sum())
        neu = int((sub["sentimento_previsto"] == "Neutra").sum())
        neg = int((sub["sentimento_previsto"] == "Negativa").sum())
        perc_pos = (pos / total) * 100
        resumo.append({"produto": prod, "total": total, "pos": pos, "neu": neu, "neg": neg, "perc_pos": perc_pos})
        print(f"  - {prod:<13}: {perc_pos:>5.1f}% positivas ({pos}/{total}) | Neutras: {neu} | Negativas: {neg}")

    df_resumo = pd.DataFrame(resumo).sort_values("perc_pos", ascending=False)

    reclamacoes = df_novas[df_novas["sentimento_previsto"] == "Negativa"]
    top_palavras = contar_palavras(reclamacoes["texto_avaliacao"], top_n=10)

    print("\n2) PALAVRAS QUE MAIS APARECEM NAS RECLAMACOES (GERAL):")
    print("-" * 58)
    for palavra, qtd in top_palavras:
        print(f"  - {palavra:<14}: {qtd} vezes")

    print("\n3) PRINCIPAIS PALAVRAS NAS RECLAMACOES POR PRODUTO:")
    print("-" * 58)
    for prod in PRODUTOS:
        rec_prod = reclamacoes[reclamacoes["produto"] == prod]["texto_avaliacao"]
        termos = ", ".join([f"{p} ({c}x)" for p, c in contar_palavras(rec_prod, top_n=4)])
        print(f"  - {prod:<13}: {termos}")
    print("=" * 58)

    # 5. Graficos Simples para o Relatorio
    # Grafico 1: Matriz de Confusao
    cm = confusion_matrix(y_test, y_pred, labels=classes)
    plt.figure(figsize=(6, 4.8))
    plt.imshow(cm, cmap="Blues")
    plt.colorbar(label="Quantidade")
    plt.xticks(range(3), classes)
    plt.yticks(range(3), classes)
    for i in range(3):
        for j in range(3):
            plt.text(j, i, str(cm[i, j]), ha="center", va="center", fontweight="bold")
    plt.xlabel("Previsto pelo Modelo")
    plt.ylabel("Real (Estrelas)")
    plt.title(f"Matriz de Confusão (Acurácia = {acuracia * 100:.1f}%)")
    plt.tight_layout()
    plt.savefig("graficos/1_matriz_confusao.png", dpi=300)
    plt.close()

    # Grafico 2: Percentual de Avaliacoes Positivas por Produto
    plt.figure(figsize=(7.5, 4.8))
    barras = plt.bar(df_resumo["produto"], df_resumo["perc_pos"], color=["#16a34a", "#2563eb", "#eab308", "#dc2626"], edgecolor="black")
    for b in barras:
        h = b.get_height()
        plt.text(b.get_x() + b.get_width() / 2, h + 1.2, f"{h:.1f}%", ha="center", fontweight="bold")
    plt.ylabel("Avaliações Positivas (%)")
    plt.ylim(0, 100)
    plt.title("Percentual de Avaliações Positivas por Produto (150 Novas)")
    plt.tight_layout()
    plt.savefig("graficos/2_percentual_positivas_produto.png", dpi=300)
    plt.close()

    # Grafico 3: Palavras mais frequentes nas Reclamacoes
    plt.figure(figsize=(7.5, 4.8))
    palavras = [p for p, _ in top_palavras][::-1]
    contagens = [c for _, c in top_palavras][::-1]
    plt.barh(palavras, contagens, color="#dc2626", edgecolor="black")
    plt.xlabel("Quantidade de Ocorrências")
    plt.title("Palavras que Mais Aparecem nas Reclamações")
    plt.tight_layout()
    plt.savefig("graficos/3_palavras_reclamacoes.png", dpi=300)
    plt.close()

    print("\nGraficos salvos na pasta 'graficos/'.")


if __name__ == "__main__":
    main()
