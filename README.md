# 🎵 Dashboard Spotify 

Este projeto  foi desenvolvido como avaliação prática para a disciplina de Probabilidade e Estatística. O sistema processa uma base de dados robusta do Spotify (mais de 113.000 faixas e 31.000 artistas) para fornecer uma plataforma de análise exploratória de dados (EDA) totalmente dinâmica. 

O objetivo principal é permitir a investigação estatística autónoma, identificando padrões de consumo, distribuições de frequência, e correlações lineares entre propriedades acústicas e popularidade, garantindo a imparcialidade analítica.
<img width="1365" height="644" alt="image" src="https://github.com/user-attachments/assets/1a4ffe24-1a3f-441e-968a-2dcd6732178a" />



## 🎛️ Motor de Filtragem Dinâmica (Barra Lateral)
<img width="239" height="642" alt="image" src="https://github.com/user-attachments/assets/27d0bebe-ad6f-4c1b-9d49-1c0c91d5b326" />

O painel lateral atua como o motor de afunilamento de dados em tempo real. O utilizador pode segmentar a base global utilizando múltiplos parâmetros simultâneos:
* **Género musical:** Caixa de seleção múltipla (ex: pop, rock, acoustic).
* **Conteúdo explícito:** Filtragem binária (Músicas com ou sem restrição de idade).
* **Top N Rankings:** *Slider* ajustável que define o limite de entidades a serem exibidas (ex: Top 10, Top 11)
* **Duração (minutos):** *Slider* de intervalo contínuo, mapeando faixas de 0.14 a 87.28 minutos
* **Popularidade:** *Slider* de intervalo paramétrico (0 a 100)

## 📊 Arquitetura Analítica (Abas de Exploração)

O painel está estruturado em seis eixos de análise estatística interativa:
<img width="1127" height="323" alt="image" src="https://github.com/user-attachments/assets/12f9cc5f-745d-4bc4-9b2d-0e2410d0e92f" />


### 1. Visão Geral
Atua como o resumo executivo dos dados populacionais filtrados. Apresenta *cards* de métricas de alto nível (Total de Registos, Artistas, Popularidade Média e Duração Média).Utiliza gráficos de barras horizontais para ranquear a frequência bruta de géneros musicais e avaliar o impacto do conteúdo explícito no volume do catálogo.

### 2. Rankings
Focado no ranqueamento ponderado. Permite ao utilizador alternar dinamicamente entre rankings de artistas, álbuns ou músicas. O algoritmo agrupa as entidades e calcula a popularidade média, garantindo relevância estatística ao exigir um mínimo de faixas por álbum/artista antes de os listar no Top N (ex: Ranquear artistas consolidados como Harry Styles e Olivia Rodrigo)

### 3. Raio-X de Artista
Uma aba de microanálise dedicada à dissecação de portefólios individuais. Ao selecionar um artista específico (ex: `!nvite`), o sistema isola exclusivamente os seus dados estatísticos (Quantidade de músicas, Álbuns, Popularidade Média). Renderiza gráficos dedicados para identificar os maiores picos de popularidade dentro da discografia daquele artista específico.

### 4. Distribuições (Análise de Dispersão e Outliers)
Essencial para a validação de hipóteses estatísticas:
* **Histogramas de Frequência:** Analisa a densidade populacional das variáveis contínuas, evidenciando a assimetria na distribuição da Duração das Músicas e da Popularidade global.


* **Boxplots (Diagramas de Caixa):** Segmenta a popularidade pelo género musical. Permite identificar rapidamente a mediana de cada estilo e localizar visualmente todos os *outliers* (pontos anómalos que fogem do limite superior ou inferior da variância normal).

<img width="1130" height="423" alt="image" src="https://github.com/user-attachments/assets/6fefe2fd-a1ec-4817-9e9b-61cc6d66efbd" />

### 5. Relações (Correlações e Cruzamentos)
O núcleo de análise multivariável:
* **Cruzamento Customizável:** Permite selecionar qualquer par de variáveis numéricas (ex: Eixo X = Energia, Eixo Y = Dançabilidade). O sistema fragmenta o Eixo X em faixas de distribuição e calcula a média do Eixo Y para cada faixa, revelando tendências de progressão (ex: como o aumento da energia afeta diretamente a propensão de uma música ser dançável).
  
* **Matriz de Correlação (Heatmap):** Processa o coeficiente de correlação de Pearson para todas as variáveis contínuas simultaneamente, permitindo identificar à primeira vista quais as propriedades de áudio que possuem ligações fortes (próximas de 1 ou -1) ou fracas.

### 6. Extração de Dados
Para garantir total transparência, exibe a *dataframe* resultante de todos os filtros aplicados numa tabela interativa. Inclui um módulo de exportação para que o utilizador descarregue o recorte de dados em formato CSV para modelagem externa.
<img width="1366" height="644" alt="image" src="https://github.com/user-attachments/assets/5dbadc9f-7d86-470d-ae6c-69df92acec4b" />



## 💻 Tecnologias Empregadas

* **Linguagem:** Python 3
* **Manipulação de Dataframes:** pandas
* **Visualização Analítica Interativa:** plotly.express
* **Framework de Interface Web:** streamlit

---

## 🚀 Guia de Execução Local

1. Clone o repositório para o seu ambiente local:
2. Instale as bibliotecas necessárias:
   pip install -r requirements.txt
3. Certifique-se de que o ficheiro dataset.csv original foi adicionado à raiz do projeto
4. Inicialize o servidor Streamlit:
   python3 -m streamlit run spotify.py
## 🤖 USO DE INTELIGÊNCIA ARTIFICIAL

Durante o desenvolvimento deste projeto, a ferramenta Gemini foi utilizada como assistente de programação e apoio estatístico. O uso da IA teve como foco principal:
- Refatorar lógicas complexas de filtragem e agrupamento de dados na biblioteca Pandas.
- Estruturar a renderização dos componentes visuais interativos no Plotly e Streamlit.
- Assegurar o cumprimento rigoroso da restrição técnica de **código sem comentários**, auxiliando na arquitetura de uma nomenclatura semântica extrema onde as variáveis explicam a própria lógica.

**EXEMPLOS DO USO PRÁTICO COM A IA:**

**Exemplo 1 — Nomenclatura Semântica e Tratamento de Dados**
python
colunas_identificacao_musica = ["artists", "album_name", "track_name"]
dados_sem_valores_ausentes = dados_sem_colunas_inuteis.dropna(subset=colunas_identificacao_musica)

---
*Projeto desenvolvido por Alycia Brasil, Francinetti Pessoa e Paulo Amaral (Engenharia de Computação,EC4MA).*
