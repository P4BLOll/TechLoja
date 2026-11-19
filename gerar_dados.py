import random
import numpy as np
import pandas as pd

PRODUTOS = ["Fone", "Smartwatch", "Caixa de Som", "Carregador"]

FRASES = {
    "Fone": {
        "Positiva": [
            "Excelente fone, som muito limpo e a bateria dura o dia todo.",
            "Adorei o áudio, cancelamento de ruído ótimo e muito confortável.",
            "Ótimo custo benefício, conecta rápido no bluetooth e tem bons graves.",
            "Fone maravilhoso, som alto e cristalino, bateria dura bastante.",
        ],
        "Neutra": [
            "O fone é razoável pelo preço, cumpre o básico para o dia a dia.",
            "Produto mediano, o som é aceitável mas o material é simples.",
            "Fone regular, funciona normal porém esperava um pouco mais.",
        ],
        "Negativa": [
            "Péssimo fone, tem chiado constante e a bateria acaba rápido.",
            "Horrível, o bluetooth desconecta sozinho e o microfone é baixo.",
            "Parou de funcionar um lado, áudio com muito chiado e bateria fraca.",
            "Não recomendo, bateria descarrega rápido, áudio baixo e com chiado.",
        ],
    },
    "Smartwatch": {
        "Positiva": [
            "Smartwatch excelente, tela brilhante e bateria dura vários dias.",
            "Adorei o relógio, sincroniza rápido com o celular e é muito bonito.",
            "Ótimo para treinos, sensores precisos e pulseira confortável.",
            "Recomendo muito, relógio rápido, tela nítida e ótima bateria.",
        ],
        "Neutra": [
            "Smartwatch mediano, mostra as notificações mas a bateria é comum.",
            "Relógio regular, cumpre o básico pelo valor pago.",
            "Razoável, funciona para ver horas e mensagens sem grandes destaques.",
        ],
        "Negativa": [
            "Péssimo smartwatch, o aplicativo não sincroniza e a tela fica travando.",
            "Horrível, a bateria acaba rápido, a pulseira soltou e trava muito.",
            "Não recomendo, perde conexão com o aplicativo e a tela fica travando.",
            "Relógio com defeito, não sincroniza no celular e a pulseira quebrou.",
        ],
    },
    "Caixa de Som": {
        "Positiva": [
            "Caixa de som excelente, volume alto, som limpo e graves potentes.",
            "Adorei a caixa, bateria dura muitas horas e o bluetooth é ótimo.",
            "Som forte e sem ruídos, ótimo custo benefício, recomendo demais.",
            "Qualidade de áudio incrível, não distorce e tem ótima bateria.",
        ],
        "Neutra": [
            "Caixa de som mediana, boa para quarto pequeno mas volume normal.",
            "Produto regular, cumpre o básico pelo preço cobrado.",
            "Som razoável, falta um pouco de grave mas funciona normal.",
        ],
        "Negativa": [
            "Caixa de som horrível, o áudio distorce no volume alto e tem chiado.",
            "Péssima, som abafado, sem grave e a bateria não segura carga.",
            "Não recomendo, apresenta chiado constante e o som distorce tudo.",
            "Muito ruim, volume baixo, áudio distorce e bateria dura pouco.",
        ],
    },
    "Carregador": {
        "Positiva": [
            "Carregador excelente, carrega muito rápido e não esquenta.",
            "Ótimo carregador turbo, cabo resistente e carregamento seguro.",
            "Recomendo, carrega o celular super rápido e tem ótima qualidade.",
            "Funciona perfeitamente, recarga veloz e material bem firme.",
        ],
        "Neutra": [
            "Carregador regular, carrega em velocidade normal e o cabo é curto.",
            "Produto mediano, cumpre o básico mas não achei tão rápido.",
            "Razoável pelo preço, funciona normal para carregar à noite.",
        ],
        "Negativa": [
            "Perigoso, o carregador esquenta muito na tomada e carrega lento.",
            "Péssimo carregador, o cabo deu mau contato e parou de funcionar.",
            "Não recomendo, esquenta demais, carregamento lento e mau contato.",
            "Horrível, parou de carregar na primeira semana e o cabo quebrou.",
        ],
    },
}


def classificar_estrelas(estrelas: int) -> str:
    if estrelas >= 4:
        return "Positiva"
    elif estrelas == 3:
        return "Neutra"
    return "Negativa"


def gerar_avaliacoes_antigas(n_avaliacoes: int = 400, seed: int = 42) -> pd.DataFrame:
    rng = random.Random(seed)
    np.random.seed(seed)

    dados = []
    for i in range(1, n_avaliacoes + 1):
        produto = PRODUTOS[(i - 1) % len(PRODUTOS)]
        estrelas = int(np.random.choice([1, 2, 3, 4, 5], p=[0.15, 0.17, 0.18, 0.25, 0.25]))
        sentimento = classificar_estrelas(estrelas)
        texto = rng.choice(FRASES[produto][sentimento])
        dados.append({
            "id_avaliacao": i,
            "produto": produto,
            "texto_avaliacao": texto,
            "estrelas": estrelas,
            "sentimento": sentimento,
        })

    return pd.DataFrame(dados).sample(frac=1.0, random_state=seed).reset_index(drop=True)


def gerar_avaliacoes_novas(n_avaliacoes: int = 150, seed: int = 100) -> pd.DataFrame:
    rng = random.Random(seed)
    np.random.seed(seed)

    # Probabilidades [Positiva, Neutra, Negativa] de cada produto no lote novo
    perfil_novas = {
        "Caixa de Som": [0.78, 0.08, 0.14],
        "Fone": [0.70, 0.15, 0.15],
        "Smartwatch": [0.63, 0.13, 0.24],
        "Carregador": [0.47, 0.19, 0.34],
    }

    dados = []
    for i in range(1, n_avaliacoes + 1):
        produto = PRODUTOS[(i - 1) % len(PRODUTOS)]
        sent = str(np.random.choice(["Positiva", "Neutra", "Negativa"], p=perfil_novas[produto]))
        texto = rng.choice(FRASES[produto][sent])
        dados.append({
            "id_avaliacao": i,
            "produto": produto,
            "texto_avaliacao": texto,
        })

    return pd.DataFrame(dados)


if __name__ == "__main__":
    df_antigas = gerar_avaliacoes_antigas(400)
    df_novas = gerar_avaliacoes_novas(150)
    df_antigas.to_csv("avaliacoes_antigas.csv", index=False, encoding="utf-8")
    df_novas.to_csv("avaliacoes_novas.csv", index=False, encoding="utf-8")
    print("Arquivos 'avaliacoes_antigas.csv' (400) e 'avaliacoes_novas.csv' (150) gerados!")
