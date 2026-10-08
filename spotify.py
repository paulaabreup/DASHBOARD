import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Exploração de Dados Musicais",
    page_icon="🎵",
    layout="wide"
)

nome_arquivo_dados_spotify = "dataset.csv"

dados_brutos_musicas = pd.read_csv(
    nome_arquivo_dados_spotify
)

colunas_sem_relevancia_analitica = [
    "Unnamed: 0"
]

dados_sem_colunas_inuteis = dados_brutos_musicas.drop(
    columns=colunas_sem_relevancia_analitica
)

colunas_identificacao_musica = [
    "artists",
    "album_name",
    "track_name"
]

dados_sem_valores_ausentes = (
    dados_sem_colunas_inuteis.dropna(
        subset=colunas_identificacao_musica
    )
)

dados_sem_duplicatas = (
    dados_sem_valores_ausentes.drop_duplicates()
)

dados_tratados = dados_sem_duplicatas.copy()

dados_tratados["duration_min"] = (
    dados_tratados["duration_ms"] / 60000
)

st.title("Exploração de Dados Musicais")

st.sidebar.header("Filtros")

lista_generos_musicais_disponiveis = sorted(
    dados_tratados["track_genre"].unique()
)

generos_musicais_selecionados = st.sidebar.multiselect(
    "Gênero musical:",
    options=lista_generos_musicais_disponiveis
)

opcao_conteudo_explicito = st.sidebar.selectbox(
    "Conteúdo explícito:",
    options=[
        "Todos",
        "Explícitas",
        "Não explícitas"
    ]
)

quantidade_top_n = st.sidebar.slider(
    "Quantidade de itens nos rankings:",
    min_value=5,
    max_value=20,
    value=10
)

duracao_minima_dataset = float(
    dados_tratados["duration_min"].min()
)

duracao_maxima_dataset = float(
    dados_tratados["duration_min"].max()
)

intervalo_duracao = st.sidebar.slider(
    "Duração da música (minutos):",
    min_value=duracao_minima_dataset,
    max_value=duracao_maxima_dataset,
    value=(
        duracao_minima_dataset,
        duracao_maxima_dataset
    )
)

popularidade_minima_dataset = int(
    dados_tratados["popularity"].min()
)

popularidade_maxima_dataset = int(
    dados_tratados["popularity"].max()
)

intervalo_popularidade = st.sidebar.slider(
    "Popularidade:",
    min_value=popularidade_minima_dataset,
    max_value=popularidade_maxima_dataset,
    value=(
        popularidade_minima_dataset,
        popularidade_maxima_dataset
    )
)

dados_filtrados = dados_tratados.copy()

if generos_musicais_selecionados:
    dados_filtrados = dados_filtrados[
        dados_filtrados["track_genre"].isin(
            generos_musicais_selecionados
        )
    ]

if opcao_conteudo_explicito == "Explícitas":
    dados_filtrados = dados_filtrados[
        dados_filtrados["explicit"] == True
    ]

elif opcao_conteudo_explicito == "Não explícitas":
    dados_filtrados = dados_filtrados[
        dados_filtrados["explicit"] == False
    ]

dados_filtrados = dados_filtrados[
    dados_filtrados["duration_min"].between(
        intervalo_duracao[0],
        intervalo_duracao[1]
    )
]

dados_filtrados = dados_filtrados[
    dados_filtrados["popularity"].between(
        intervalo_popularidade[0],
        intervalo_popularidade[1]
    )
]

if dados_filtrados.empty:
    st.warning(
        "Nenhum registro encontrado para os filtros selecionados."
    )
    st.stop()

quantidade_registros_filtrados = len(
    dados_filtrados
)

quantidade_artistas_filtrados = (
    dados_filtrados["artists"].nunique()
)

popularidade_media_filtrada = (
    dados_filtrados["popularity"].mean()
)

duracao_media_filtrada = (
    dados_filtrados["duration_min"].mean()
)

coluna_registros, coluna_artistas, coluna_popularidade, coluna_duracao = (
    st.columns(4)
)

coluna_registros.metric(
    "Registros",
    quantidade_registros_filtrados
)

coluna_artistas.metric(
    "Artistas",
    quantidade_artistas_filtrados
)

coluna_popularidade.metric(
    "Popularidade média",
    f"{popularidade_media_filtrada:.1f}"
)

coluna_duracao.metric(
    "Duração média",
    f"{duracao_media_filtrada:.2f} min"
)

(
    aba_visao_geral,
    aba_rankings,
    aba_artista,
    aba_distribuicoes,
    aba_relacoes,
    aba_dados
) = st.tabs(
    [
        "Visão Geral",
        "Rankings",
        "Artista",
        "Distribuições",
        "Relações",
        "Dados"
    ]
)

with aba_visao_geral:
    st.subheader(
        "Quantidade de Registros por Gênero"
    )

    quantidade_por_genero = (
        dados_filtrados["track_genre"]
        .value_counts()
        .head(15)
        .reset_index()
    )

    quantidade_por_genero.columns = [
        "track_genre",
        "quantidade"
    ]

    grafico_quantidade_genero = px.bar(
        quantidade_por_genero,
        x="quantidade",
        y="track_genre",
        orientation="h",
        labels={
            "quantidade": "Quantidade de registros",
            "track_genre": "Gênero"
        },
        title="Gêneros com Maior Quantidade de Registros"
    )

    grafico_quantidade_genero.update_layout(
        yaxis={
            "categoryorder": "total ascending"
        }
    )

    st.plotly_chart(
        grafico_quantidade_genero,
        use_container_width=True
    )

    st.subheader(
        "Distribuição de Conteúdo Explícito"
    )

    quantidade_por_conteudo_explicito = (
        dados_filtrados["explicit"]
        .value_counts()
        .reset_index()
    )

    quantidade_por_conteudo_explicito.columns = [
        "explicit",
        "quantidade"
    ]

    quantidade_por_conteudo_explicito[
        "explicit"
    ] = quantidade_por_conteudo_explicito[
        "explicit"
    ].map(
        {
            True: "Explícita",
            False: "Não explícita"
        }
    )

    grafico_conteudo_explicito = px.bar(
        quantidade_por_conteudo_explicito,
        x="explicit",
        y="quantidade",
        labels={
            "explicit": "Classificação",
            "quantidade": "Quantidade de músicas"
        },
        title="Músicas Explícitas e Não Explícitas"
    )

    st.plotly_chart(
        grafico_conteudo_explicito,
        use_container_width=True
    )

    st.subheader(
        "Popularidade Média por Conteúdo Explícito"
    )

    popularidade_por_conteudo = (
        dados_filtrados
        .groupby("explicit")["popularity"]
        .mean()
        .reset_index()
    )

    popularidade_por_conteudo[
        "explicit"
    ] = popularidade_por_conteudo[
        "explicit"
    ].map(
        {
            True: "Explícita",
            False: "Não explícita"
        }
    )

    grafico_popularidade_conteudo = px.bar(
        popularidade_por_conteudo,
        x="explicit",
        y="popularity",
        labels={
            "explicit": "Classificação",
            "popularity": "Popularidade média"
        },
        title="Popularidade Média por Classificação"
    )

    st.plotly_chart(
        grafico_popularidade_conteudo,
        use_container_width=True
    )


with aba_rankings:
    st.subheader("Rankings")

    tipo_ranking = st.radio(
        "Escolha o ranking:",
        options=[
            "Artistas",
            "Álbuns",
            "Músicas"
        ],
        horizontal=True
    )

    if tipo_ranking == "Artistas":
        dados_unicos_por_artista = (
            dados_filtrados.drop_duplicates(
                subset=[
                    "artists",
                    "track_id"
                ]
            )
        )

        popularidade_media_por_artista = (
            dados_unicos_por_artista
            .groupby("artists")
            .agg(
                popularidade_media=(
                    "popularity",
                    "mean"
                ),
                quantidade_musicas=(
                    "track_id",
                    "nunique"
                )
            )
            .reset_index()
        )

        popularidade_media_por_artista = (
            popularidade_media_por_artista[
                popularidade_media_por_artista[
                    "quantidade_musicas"
                ] >= 3
            ]
        )

        artistas_mais_populares = (
            popularidade_media_por_artista
            .sort_values(
                by="popularidade_media",
                ascending=False
            )
            .head(quantidade_top_n)
        )

        grafico_artistas_mais_populares = px.bar(
            artistas_mais_populares,
            x="popularidade_media",
            y="artists",
            orientation="h",
            hover_data=[
                "quantidade_musicas"
            ],
            labels={
                "popularidade_media":
                    "Popularidade média",
                "artists":
                    "Artista",
                "quantidade_musicas":
                    "Quantidade de músicas"
            },
            title=(
                f"Top {quantidade_top_n} Artistas "
                "por Popularidade Média"
            )
        )

        grafico_artistas_mais_populares.update_layout(
            yaxis={
                "categoryorder": "total ascending"
            }
        )

        st.plotly_chart(
            grafico_artistas_mais_populares,
            use_container_width=True
        )

    elif tipo_ranking == "Álbuns":
        dados_unicos_por_album = (
            dados_filtrados.drop_duplicates(
                subset=[
                    "album_name",
                    "artists",
                    "track_id"
                ]
            )
        )

        popularidade_media_por_album = (
            dados_unicos_por_album
            .groupby(
                [
                    "album_name",
                    "artists"
                ]
            )
            .agg(
                popularidade_media=(
                    "popularity",
                    "mean"
                ),
                quantidade_musicas=(
                    "track_id",
                    "nunique"
                )
            )
            .reset_index()
        )

        popularidade_media_por_album = (
            popularidade_media_por_album[
                popularidade_media_por_album[
                    "quantidade_musicas"
                ] >= 3
            ]
        )

        albuns_mais_populares = (
            popularidade_media_por_album
            .sort_values(
                by="popularidade_media",
                ascending=False
            )
            .head(quantidade_top_n)
        )

        grafico_albuns_mais_populares = px.bar(
            albuns_mais_populares,
            x="popularidade_media",
            y="album_name",
            orientation="h",
            hover_data=[
                "artists",
                "quantidade_musicas"
            ],
            labels={
                "popularidade_media":
                    "Popularidade média",
                "album_name":
                    "Álbum",
                "artists":
                    "Artista",
                "quantidade_musicas":
                    "Quantidade de músicas"
            },
            title=(
                f"Top {quantidade_top_n} Álbuns "
                "por Popularidade Média"
            )
        )

        grafico_albuns_mais_populares.update_layout(
            yaxis={
                "categoryorder": "total ascending"
            }
        )

        st.plotly_chart(
            grafico_albuns_mais_populares,
            use_container_width=True
        )

    elif tipo_ranking == "Músicas":
        musicas_mais_populares = (
            dados_filtrados
            .drop_duplicates(
                subset=["track_id"]
            )[
                [
                    "track_name",
                    "artists",
                    "popularity"
                ]
            ]
            .sort_values(
                by="popularity",
                ascending=False
            )
            .head(quantidade_top_n)
        )

        grafico_musicas_mais_populares = px.bar(
            musicas_mais_populares,
            x="popularity",
            y="track_name",
            orientation="h",
            hover_data=[
                "artists"
            ],
            labels={
                "popularity":
                    "Popularidade",
                "track_name":
                    "Música",
                "artists":
                    "Artista"
            },
            title=(
                f"Top {quantidade_top_n} Músicas "
                "por Popularidade"
            )
        )

        grafico_musicas_mais_populares.update_layout(
            yaxis={
                "categoryorder": "total ascending"
            }
        )

        st.plotly_chart(
            grafico_musicas_mais_populares,
            use_container_width=True
        )


with aba_artista:
    st.subheader("Exploração por Artista")

    lista_artistas_disponiveis = sorted(
        dados_filtrados["artists"].unique()
    )

    artista_selecionado = st.selectbox(
        "Selecione um artista:",
        options=lista_artistas_disponiveis
    )

    dados_artista_selecionado = (
        dados_filtrados[
            dados_filtrados["artists"]
            == artista_selecionado
        ]
    )

    dados_artista_sem_repeticao = (
        dados_artista_selecionado.drop_duplicates(
            subset=["track_id"]
        )
    )

    quantidade_musicas_artista = (
        dados_artista_sem_repeticao[
            "track_id"
        ].nunique()
    )

    quantidade_albuns_artista = (
        dados_artista_sem_repeticao[
            "album_name"
        ].nunique()
    )

    popularidade_media_artista = (
        dados_artista_sem_repeticao[
            "popularity"
        ].mean()
    )

    coluna_musicas, coluna_albuns, coluna_popularidade_artista = (
        st.columns(3)
    )

    coluna_musicas.metric(
        "Músicas",
        quantidade_musicas_artista
    )

    coluna_albuns.metric(
        "Álbuns",
        quantidade_albuns_artista
    )

    coluna_popularidade_artista.metric(
        "Popularidade média",
        f"{popularidade_media_artista:.1f}"
    )

    st.subheader(
        f"Músicas Mais Populares de {artista_selecionado}"
    )

    musicas_populares_artista = (
        dados_artista_sem_repeticao[
            [
                "track_name",
                "popularity"
            ]
        ]
        .sort_values(
            by="popularity",
            ascending=False
        )
        .head(quantidade_top_n)
    )

    grafico_musicas_artista = px.bar(
        musicas_populares_artista,
        x="popularity",
        y="track_name",
        orientation="h",
        labels={
            "popularity": "Popularidade",
            "track_name": "Música"
        },
        title=(
            f"Top {quantidade_top_n} Músicas de "
            f"{artista_selecionado}"
        )
    )

    grafico_musicas_artista.update_layout(
        yaxis={
            "categoryorder": "total ascending"
        }
    )

    st.plotly_chart(
        grafico_musicas_artista,
        use_container_width=True
    )

    st.subheader(
        f"Álbuns de {artista_selecionado}"
    )

    albuns_artista = (
        dados_artista_sem_repeticao
        .groupby("album_name")
        .agg(
            popularidade_media=(
                "popularity",
                "mean"
            ),
            quantidade_musicas=(
                "track_id",
                "nunique"
            )
        )
        .reset_index()
        .sort_values(
            by="popularidade_media",
            ascending=False
        )
        .head(quantidade_top_n)
    )

    grafico_albuns_artista = px.bar(
        albuns_artista,
        x="popularidade_media",
        y="album_name",
        orientation="h",
        hover_data=[
            "quantidade_musicas"
        ],
        labels={
            "popularidade_media":
                "Popularidade média",
            "album_name":
                "Álbum",
            "quantidade_musicas":
                "Quantidade de músicas"
        },
        title=(
            f"Álbuns de {artista_selecionado} "
            "por Popularidade Média"
        )
    )

    grafico_albuns_artista.update_layout(
        yaxis={
            "categoryorder": "total ascending"
        }
    )

    st.plotly_chart(
        grafico_albuns_artista,
        use_container_width=True
    )


with aba_distribuicoes:
    st.subheader(
        "Distribuição de Popularidade"
    )

    grafico_distribuicao_popularidade = px.histogram(
        dados_filtrados,
        x="popularity",
        nbins=20,
        labels={
            "popularity": "Popularidade"
        }
    )

    grafico_distribuicao_popularidade.update_layout(
        yaxis_title="Quantidade de registros"
    )

    st.plotly_chart(
        grafico_distribuicao_popularidade,
        use_container_width=True
    )

    st.subheader(
        "Distribuição da Popularidade por Gênero"
    )

    generos_para_boxplot = (
        dados_filtrados["track_genre"]
        .value_counts()
        .head(10)
        .index
    )

    dados_boxplot = dados_filtrados[
        dados_filtrados["track_genre"].isin(
            generos_para_boxplot
        )
    ]

    grafico_boxplot_popularidade = px.box(
        dados_boxplot,
        x="track_genre",
        y="popularity",
        labels={
            "track_genre": "Gênero musical",
            "popularity": "Popularidade"
        }
    )

    st.plotly_chart(
        grafico_boxplot_popularidade,
        use_container_width=True
    )

    st.subheader(
        "Distribuição da Duração das Músicas"
    )

    grafico_distribuicao_duracao = px.histogram(
        dados_filtrados,
        x="duration_min",
        nbins=30,
        labels={
            "duration_min": "Duração (minutos)"
        }
    )

    grafico_distribuicao_duracao.update_layout(
        yaxis_title="Quantidade de registros"
    )

    st.plotly_chart(
        grafico_distribuicao_duracao,
        use_container_width=True
    )


with aba_relacoes:
    st.subheader(
        "Relação entre Variáveis Musicais"
    )

    variaveis_numericas_para_analise = {
        "Popularidade": "popularity",
        "Duração": "duration_min",
        "Dançabilidade": "danceability",
        "Energia": "energy",
        "Loudness": "loudness",
        "Speechiness": "speechiness",
        "Acousticness": "acousticness",
        "Instrumentalness": "instrumentalness",
        "Liveness": "liveness",
        "Valence": "valence",
        "Tempo": "tempo"
    }

    coluna_variavel_x, coluna_variavel_y = (
        st.columns(2)
    )

    nome_variavel_x = coluna_variavel_x.selectbox(
        "Variável do eixo X",
        options=list(
            variaveis_numericas_para_analise.keys()
        ),
        index=3
    )

    nome_variavel_y = coluna_variavel_y.selectbox(
        "Variável do eixo Y",
        options=list(
            variaveis_numericas_para_analise.keys()
        ),
        index=2
    )

    variavel_x = (
        variaveis_numericas_para_analise[
            nome_variavel_x
        ]
    )

    variavel_y = (
        variaveis_numericas_para_analise[
            nome_variavel_y
        ]
    )

    if variavel_x != variavel_y:
        dados_relacao_variaveis = (
            dados_filtrados[
                [
                    variavel_x,
                    variavel_y
                ]
            ]
            .dropna()
            .copy()
        )

        dados_relacao_variaveis[
            "faixa_variavel_x"
        ] = pd.cut(
            dados_relacao_variaveis[
                variavel_x
            ],
            bins=5,
            duplicates="drop"
        )

        media_variavel_y_por_faixa = (
            dados_relacao_variaveis
            .groupby(
                "faixa_variavel_x",
                observed=True
            )[variavel_y]
            .mean()
            .reset_index()
        )

        media_variavel_y_por_faixa[
            "faixa_variavel_x"
        ] = media_variavel_y_por_faixa[
            "faixa_variavel_x"
        ].astype(str)

        grafico_relacao_variaveis = px.bar(
            media_variavel_y_por_faixa,
            x="faixa_variavel_x",
            y=variavel_y,
            labels={
                "faixa_variavel_x":
                    nome_variavel_x,
                variavel_y:
                    f"Média de {nome_variavel_y}"
            },
            title=(
                f"Média de {nome_variavel_y} "
                f"por Faixa de {nome_variavel_x}"
            )
        )

        st.plotly_chart(
            grafico_relacao_variaveis,
            use_container_width=True
        )

    else:
        st.info(
            "Selecione duas variáveis diferentes."
        )

    st.subheader("Matriz de Correlação")

    colunas_correlacao = [
        "popularity",
        "duration_min",
        "danceability",
        "energy",
        "loudness",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo"
    ]

    matriz_correlacao = (
        dados_filtrados[
            colunas_correlacao
        ].corr()
    )

    grafico_correlacao = px.imshow(
        matriz_correlacao,
        text_auto=".2f",
        aspect="auto",
        labels={
            "color": "Correlação"
        },
        title="Correlação entre Variáveis Musicais"
    )

    st.plotly_chart(
        grafico_correlacao,
        use_container_width=True
    )


with aba_dados:
    st.subheader("Dados Filtrados")

    colunas_exibidas = [
        "artists",
        "track_name",
        "album_name",
        "track_genre",
        "popularity",
        "duration_min",
        "explicit",
        "danceability",
        "energy",
        "valence",
        "tempo"
    ]

    dados_para_exibicao = (
        dados_filtrados[
            colunas_exibidas
        ].copy()
    )

    dados_para_exibicao = (
        dados_para_exibicao.rename(
            columns={
                "artists": "Artista",
                "track_name": "Música",
                "album_name": "Álbum",
                "track_genre": "Gênero",
                "popularity": "Popularidade",
                "duration_min": "Duração (min)",
                "explicit": "Explícita",
                "danceability": "Dançabilidade",
                "energy": "Energia",
                "valence": "Valence",
                "tempo": "Tempo"
            }
        )
    )

    st.dataframe(
        dados_para_exibicao,
        use_container_width=True
    )

    arquivo_dados_filtrados = (
        dados_para_exibicao.to_csv(
            index=False
        ).encode("utf-8")
    )

    st.download_button(
        label="Baixar dados filtrados",
        data=arquivo_dados_filtrados,
        file_name="dados_filtrados.csv",
        mime="text/csv"
    )