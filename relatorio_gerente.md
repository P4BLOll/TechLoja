# Relatório para o Gerente — TechLoja

**Integrantes:** Rebeca Matewanga • Mariana Ocireu • Pablo de Sousa  
**Base Analisada:** 150 avaliações novas (somente texto), classificadas pelo modelo **Naive Bayes (`MultinomialNB`)** treinado com 400 avaliações antigas com estrelas.

---

## 1. Percentual de Avaliações Positivas de Cada Produto

- **Caixa de Som:** **75.7%** de avaliações positivas (`28 de 37`) — *Produto mais bem avaliado da loja.*
- **Fone:** **71.1%** de avaliações positivas (`27 de 38`) — *Boa aprovação geral.*
- **Smartwatch:** **65.8%** de avaliações positivas (`25 de 38`) — *Desempenho intermediário.*
- **Carregador:** **54.1%** de avaliações positivas (`20 de 37`) — *Produto mais crítico, com maior índice de reclamações (10 negativas).*

---

## 2. Palavras que Mais Aparecem nas Reclamações

Analisando os textos das avaliações classificadas como **Negativas (Reclamações)**, os termos mais frequentes foram:

| Palavra | Ocorrências | Problema Relatado |
| :--- | :---: | :--- |
| **`parou`** | 11x | Produto parou de funcionar ou carregar na primeira semana |
| **`bateria`** | 11x | Bateria fraca ou que descarrega rápido (Fone, Smartwatch e Caixa de Som) |
| **`cabo`** | 8x | Cabo do carregador com mau contato ou que quebrou facilmente |
| **`chiado`** | 8x | Ruído e chiado constante no Fone e na Caixa de Som |
| **`áudio`** | 7x | Áudio baixo ou com falha de saída |
| **`distorce`** | 6x | Som da Caixa de Som distorce em volume alto |
| **`quebrou`** | 5x | Fragilidade física no cabo do Carregador e na pulseira do Smartwatch |
| **`acaba`** | 5x | Bateria que acaba rápido durante o uso |

### Resumo por Produto para Ação do Gerente
1. **Carregador:** Revisar fornecedor devido a falhas no **`cabo`** (`8x`), que **`parou`** de funcionar (`8x`) e apresentou **`mau contato`** (`4x`).
2. **Smartwatch:** Corrigir falhas de **`conexão`** (`4x`) com o **`aplicativo`** (`4x`) e travamentos de **`tela`** (`4x`).
3. **Fone:** Verificar lote com **`chiado`** (`5x`) e baixa duração de **`bateria`** (`5x`).
4. **Caixa de Som:** Verificar alto-falantes que **`distorcem`** (`6x`) o **`áudio`** (`4x`) em **`volume`** (`4x`) alto.
