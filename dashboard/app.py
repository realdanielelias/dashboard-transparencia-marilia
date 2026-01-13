# RU4590111 Daniel Elias de Souza

import streamlit as st
import pandas as pd
import numpy as np
import os
import duckdb
import altair as alt
import sys
import matplotlib  # Garantir que matplotlib seja importado para estilização

# Adicionar diretório pai ao caminho para importar config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATA_DIR
from utils import rename_columns, convert_numeric_columns

st.set_page_config(page_title="Dashboard Marília", layout="wide")
st.title("📊 Dashboard de Dados Públicos de Marília")

def load_csv(name):
    path = os.path.join(DATA_DIR, name)
    if os.path.exists(path):
        df = pd.read_csv(path)
        # Determina o tipo do dataset e renomeia colunas
        dataset_type = get_dataset_type(name)
        df = rename_columns(df, dataset_type)
        # Converte colunas numéricas automaticamente
        df = convert_numeric_columns(df)
        return df
    return None

datasets = {
    "Despesas da Câmara (2020-2023)": "camara_despesas_2020_2023.csv",
    "Receita Analítica da Prefeitura": "ReceitaAnalitica_dados.csv",
    "Despesas COVID da Prefeitura": "despesacovid_dados.csv",
    "Passagens da Prefeitura": "passagenslocomocao_dados.csv",
    "Investimentos da Prefeitura": "DespesaseInvestimentos_dados.csv",
    "Emendas Parlamentares da Prefeitura": "EmendasParlamentares_dados.csv"
}

# Determina o tipo do dataset para renomear colunas
def get_dataset_type(filename):
    if 'camara' in filename:
        return 'camara'
    elif 'covid' in filename:
        return 'covid'
    elif 'passagens' in filename:
        return 'passagens'
    elif 'investimentos' in filename:
        return 'investimentos'
    return 'unknown'

# Criar conexão DuckDB e registrar tabelas
conn = duckdb.connect(database=':memory:', read_only=False)

for label, file in datasets.items():
    df = load_csv(file)
    if df is not None:
        table_name = file.replace('.csv', '').replace('-', '_').replace(' ', '_').lower()
        conn.register(table_name, df)

# Barra lateral para controles
st.sidebar.header("🎛️ Controles")

# Seleção de conjunto de dados
selected_dataset = st.sidebar.selectbox(
    "Selecionar Conjunto de Dados",
    list(datasets.keys()),
    index=0
)

# Carregar conjunto de dados selecionado
df = load_csv(datasets[selected_dataset])

table_name = datasets[selected_dataset].replace('.csv', '').replace('-', '_').replace(' ', '_').lower()

if df is not None:
    st.header(f"📋 {selected_dataset}")

    # Informações básicas (serão atualizadas após aplicação dos filtros)
    # Métricas originais (antes dos filtros)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Linhas (Original)", len(df))
    with col2:
        st.metric("Total de Colunas (Original)", len(df.columns))
    with col3:
        # Só mostra anos se a coluna 'Ano' estiver presente
        if 'Ano' in df.columns:
            st.metric("Anos (Original)", len(df['Ano'].unique()))

    # Seleção de colunas
    st.subheader("🔍 Seleção de Colunas")
    selected_columns = st.multiselect(
        "Escolha as colunas para exibir:",
        df.columns.tolist(),
        default=df.columns.tolist()[:5]  # Padrão para primeiras 5 colunas
    )

    # Garantir que pelo menos uma coluna seja selecionada
    if not selected_columns:
        st.warning("⚠️ Selecione pelo menos uma coluna para continuar.")
        selected_columns = df.columns.tolist()[:1]

    # Opções de filtragem
    st.subheader("🎯 Filtros")

    # Sempre começar com df_filtered baseado apenas nas colunas selecionadas
    # Todas as métricas e gráficos devem usar apenas df_filtered
    df_filtered = df[selected_columns].copy()

    # Filtro de ano (apenas se 'Ano' estiver nas colunas selecionadas)
    if 'Ano' in df_filtered.columns:
        years = sorted(df_filtered['Ano'].unique())
        selected_years = st.multiselect("Selecionar Anos:", years, default=years)
        if selected_years:
            # Filtrar o dataframe já filtrado
            df_filtered = df_filtered[df_filtered['Ano'].isin(selected_years)]
    else:
        # Se 'Ano' não está nas colunas selecionadas, mostrar aviso
        if 'Ano' in df.columns:
            st.info("💡 Para filtrar por ano, inclua a coluna 'Ano' na seleção acima.")

    # Filtro de busca de texto (apenas em colunas de texto selecionadas)
    search_term = st.text_input("Buscar em colunas de texto:")
    if search_term:
        text_columns = df_filtered.select_dtypes(include=['object']).columns
        if len(text_columns) > 0:
            mask = pd.Series(False, index=df_filtered.index)
            for col in text_columns:
                mask |= df_filtered[col].astype(str).str.contains(search_term, case=False, na=False)
            df_filtered = df_filtered[mask]
        else:
            st.info("💡 Para busca de texto, inclua colunas de texto na seleção acima.")

    # Filtros numéricos (apenas em colunas numéricas selecionadas)
    numeric_columns = df_filtered.select_dtypes(include=['number']).columns
    if len(numeric_columns) > 0:
        filter_col = st.selectbox("Filtrar por coluna numérica:", ["Nenhuma"] + list(numeric_columns))
        if filter_col != "Nenhuma" and filter_col in df_filtered.columns:
            min_val = float(df_filtered[filter_col].min())
            max_val = float(df_filtered[filter_col].max())
            value_range = st.slider(
                f"Faixa para {filter_col}:",
                min_val, max_val,
                (min_val, max_val)
            )
            df_filtered = df_filtered[
                (df_filtered[filter_col] >= value_range[0]) &
                (df_filtered[filter_col] <= value_range[1])
            ]
    else:
        st.info("💡 Para filtros numéricos, inclua colunas numéricas na seleção acima.")

    # Informações atualizadas após filtros
    st.subheader("📊 Dados Filtrados")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Linhas Filtradas", len(df_filtered))
    with col2:
        st.metric("Colunas Selecionadas", len(df_filtered.columns))
    with col3:
        # Só mostra anos filtrados se 'Ano' estiver presente
        if 'Ano' in df_filtered.columns and len(df_filtered) > 0:
            anos_filtrados = len(df_filtered['Ano'].unique()) if not df_filtered['Ano'].isna().all() else 0
            st.metric("Anos Filtrados", anos_filtrados)

    # Exibir dados filtrados
    st.subheader("📊 Tabela de Dados")
    st.dataframe(df_filtered, width='stretch')

    # Estatísticas resumidas
    if st.checkbox("Mostrar Estatísticas Resumidas"):
        st.subheader("📈 Estatísticas Resumidas")
        st.write(df_filtered.describe())

    # Charts
    st.subheader("📊 Visualizações")

    # Verificar se há dados suficientes para visualizações
    if len(df_filtered) == 0:
        st.warning("⚠️ Nenhum dado disponível após aplicação dos filtros.")
    else:
        # Criar abas para diferentes tipos de gráficos
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Barras", "🥧 Pizza", "📈 Distribuição", "📉 Correlação", "📅 Temporal"])

        with tab1:
            st.markdown("**📊 Análise de Barras** - Distribuição de categorias")
            # Só usa colunas categóricas presentes em df_filtered
            categorical_cols = df_filtered.select_dtypes(include=['object']).columns
            if len(categorical_cols) > 0:
                col1, col2, col3 = st.columns([1.5, 1, 1])
                with col1:
                    chart_col = st.selectbox("Coluna categórica:", categorical_cols, key="bar_chart_col", index=0)
                with col2:
                    top_n = st.slider("Top N categorias:", 5, 20, 10, key="bar_top_n")
                with col3:
                    chart_type = st.selectbox("Tipo:", ["Horizontal", "Vertical", "Normalizado"], key="bar_type")

                if chart_col and chart_col in df_filtered.columns:
                    # Obter top N categorias apenas dos dados filtrados
                    top_categories = df_filtered[chart_col].value_counts().head(top_n)
                    if len(top_categories) > 0:
                        chart_data = pd.DataFrame({
                            'categoria': top_categories.index,
                            'contagem': top_categories.values
                        })

                        # Calcular percentuais
                        total = top_categories.sum()
                        chart_data['percentual'] = (chart_data['contagem'] / total * 100).round(1)

                        if chart_type == "Horizontal":
                            # Gráfico de barras horizontal
                            chart = alt.Chart(chart_data).mark_bar(
                                color='steelblue',
                                opacity=0.8
                            ).encode(
                                x=alt.X('contagem:Q', title='Contagem'),
                                y=alt.Y('categoria:N', sort='-x', title=chart_col),
                                tooltip=['categoria', 'contagem', 'percentual']
                            ).properties(height=400)
                        elif chart_type == "Vertical":
                            # Gráfico de barras vertical
                            chart = alt.Chart(chart_data).mark_bar(
                                color='steelblue',
                                opacity=0.8
                            ).encode(
                                x=alt.X('categoria:N', title=chart_col, sort='-y'),
                                y=alt.Y('contagem:Q', title='Contagem'),
                                tooltip=['categoria', 'contagem', 'percentual']
                            ).properties(height=400)
                        else:  # Normalizado
                            # Gráfico de barras normalizado (percentuais)
                            chart = alt.Chart(chart_data).mark_bar(
                                color='steelblue',
                                opacity=0.8
                            ).encode(
                                x=alt.X('percentual:Q', title='Percentual (%)'),
                                y=alt.Y('categoria:N', sort='-x', title=chart_col),
                                tooltip=['categoria', 'contagem', 'percentual']
                            ).properties(height=400)

                        st.altair_chart(chart, width='stretch')

                        # Estatísticas resumidas baseadas apenas nos dados filtrados
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Total de Categorias", len(df_filtered[chart_col].unique()))
                        with col2:
                            st.metric("Top Categoria", top_categories.index[0])
                        with col3:
                            st.metric("Contagem Top", int(top_categories.iloc[0]))
                        with col4:
                            top_percentage = (top_categories.iloc[0] / top_categories.sum()) * 100
                            st.metric("Percentual Top", f"{top_percentage:.1f}%")

                        # Tabela de detalhamento
                        st.subheader("📋 Detalhamento")
                        display_data = chart_data.copy()
                        display_data['percentual'] = display_data['percentual'].astype(str) + '%'
                        st.dataframe(
                            display_data.style.background_gradient(subset=['contagem'], cmap='Blues')
                            .format({'contagem': '{:,}', 'percentual': '{}'}),
                            width='stretch'
                        )
                    else:
                        st.info("💡 Não há dados suficientes para gerar o gráfico de barras.")
                else:
                    st.info("💡 Selecione uma coluna categórica válida para o gráfico.")
            else:
                st.info("💡 Não há colunas categóricas disponíveis nos dados filtrados.")

    with tab2:
        st.markdown("**🥧 Análise de Pizza** - Proporções das categorias")

        categorical_cols = df_filtered.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            col1, col2, col3 = st.columns([1.5, 1, 1])
            with col1:
                pie_col = st.selectbox("Coluna categórica:", categorical_cols, key="pie_chart_col", index=0)
            with col2:
                pie_limit = st.slider("Máximo de categorias:", 5, 15, 8, key="pie_limit")
            with col3:
                show_labels = st.checkbox("Mostrar rótulos", value=True, key="pie_labels")

            if pie_col and pie_col in df_filtered.columns:
                # Obter categorias principais para gráfico de pizza apenas dos dados filtrados
                pie_data = df_filtered[pie_col].value_counts().head(pie_limit)
                if len(pie_data) > 0:
                    # Adicionar categoria "Outros" se houver mais categorias
                    if len(df_filtered[pie_col].value_counts()) > pie_limit:
                        other_count = df_filtered[pie_col].value_counts().iloc[pie_limit:].sum()
                        pie_data = pd.concat([pie_data, pd.Series({'Outros': other_count})])

                    pie_df = pd.DataFrame({
                        'categoria': pie_data.index,
                        'valor': pie_data.values
                    })

                    pie_df['percentual'] = (pie_df['valor'] / pie_df['valor'].sum() * 100).round(1)

                    # Criar gráfico de pizza
                    if show_labels:
                        pie_chart = alt.Chart(pie_df).mark_arc(
                            innerRadius=50,
                            outerRadius=120
                        ).encode(
                            theta=alt.Theta('valor:Q'),
                            color=alt.Color('categoria:N',
                                scale=alt.Scale(scheme='category20'),
                                legend=alt.Legend(title=pie_col, orient='bottom')
                            ),
                            tooltip=['categoria', 'valor', 'percentual']
                        ).properties(height=350)
                    else:
                        pie_chart = alt.Chart(pie_df).mark_arc(
                            innerRadius=50,
                            outerRadius=120
                        ).encode(
                            theta=alt.Theta('valor:Q'),
                            color=alt.Color('categoria:N',
                                scale=alt.Scale(scheme='category20'),
                                legend=alt.Legend(title=pie_col, orient='bottom')
                            ),
                            tooltip=['categoria', 'valor', 'percentual']
                        ).properties(height=350)

                    st.altair_chart(pie_chart, width='stretch')

                    # Métricas resumidas baseadas apenas nos dados filtrados
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total de Categorias", len(pie_df))
                    with col2:
                        st.metric("Maior Fatia", pie_df.loc[pie_df['valor'].idxmax(), 'categoria'])
                    with col3:
                        st.metric("Percentual Maior", f"{pie_df['percentual'].max():.1f}%")
                    with col4:
                        entropy = -sum((pie_df['percentual']/100) * np.log2(pie_df['percentual']/100)) if len(pie_df) > 1 else 0
                        st.metric("Diversidade", f"{entropy:.2f}")

                    # Verificar se há categoria dominante
                    max_pct = pie_df['percentual'].max()
                    if max_pct > 50:
                        st.warning(f"⚠️ **Categoria dominante:** {pie_df.loc[pie_df['percentual'].idxmax(), 'categoria']} representa {max_pct:.1f}% do total")

                    # Tabela de detalhamento
                    st.subheader("📋 Detalhamento")
                    display_df = pie_df.copy()
                    display_df['percentual'] = display_df['percentual'].astype(str) + '%'
                    st.dataframe(
                        display_df.style.background_gradient(subset=['valor'], cmap='Oranges')
                        .format({'valor': '{:,}', 'percentual': '{}'}),
                        width='stretch'
                    )
                else:
                    st.info("💡 Não há dados suficientes para gerar o gráfico de pizza.")
            else:
                st.info("💡 Selecione uma coluna categórica válida para o gráfico.")

        else:
            st.info("💡 Não há colunas categóricas disponíveis nos dados filtrados.")

    with tab3:
        st.markdown("**📈 Distribuição** - Histogramas e análise de valores numéricos")

        numeric_columns = df_filtered.select_dtypes(include=['number']).columns
        if len(numeric_columns) > 0:
            col1, col2 = st.columns([2, 1])
            with col1:
                hist_col = st.selectbox("Coluna numérica:", numeric_columns, key="hist_col", index=0)
            with col2:
                bins = st.slider("Número de bins:", 10, 50, 20, key="hist_bins")

            if hist_col and hist_col in df_filtered.columns:
                # Remover valores NaN para o histograma
                hist_data = df_filtered[hist_col].dropna()

                if len(hist_data) > 0:
                    # Histogram
                    hist = alt.Chart(pd.DataFrame({hist_col: hist_data})).mark_bar(
                        opacity=0.7,
                        color='lightblue'
                    ).encode(
                        x=alt.X(f'{hist_col}:Q', bin=alt.Bin(maxbins=bins), title=hist_col),
                        y=alt.Y('count()', title='Frequência'),
                        tooltip=[alt.Tooltip(f'{hist_col}:Q', bin=True), 'count()']
                    ).properties(height=300)

                    st.altair_chart(hist, width='stretch')

                    # Estatísticas básicas
                    mean_val = hist_data.mean()
                    median_val = hist_data.median()
                    min_val = hist_data.min()
                    max_val = hist_data.max()

                    # Tratar valores NaN
                    mean_val = mean_val if not pd.isna(mean_val) else 0.0
                    median_val = median_val if not pd.isna(median_val) else 0.0
                    min_val = min_val if not pd.isna(min_val) else 0.0
                    max_val = max_val if not pd.isna(max_val) else 0.0

                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Média", f"{mean_val:.2f}")
                    with col2:
                        st.metric("Mediana", f"{median_val:.2f}")
                    with col3:
                        st.metric("Mín", f"{min_val:.2f}")
                    with col4:
                        st.metric("Máx", f"{max_val:.2f}")
                else:
                    st.warning("Não há dados suficientes para criar o histograma.")
        else:
            st.info("Nenhuma coluna numérica disponível para histogramas.")

    with tab4:
        st.markdown("**� Correlação** - Relacionamentos entre variáveis numéricas")

        numeric_columns = df_filtered.select_dtypes(include=['number']).columns
        categorical_cols = df_filtered.select_dtypes(include=['object']).columns

        if len(numeric_columns) >= 2:
            # Matriz de Correlação
            st.subheader("Matriz de Correlação")
            corr_matrix = df_filtered[numeric_columns].corr()

            # Heatmap
            corr_data = corr_matrix.reset_index().melt(id_vars='index')
            corr_data.columns = ['Variável 1', 'Variável 2', 'Correlação']

            heatmap = alt.Chart(corr_data).mark_rect().encode(
                x=alt.X('Variável 1:N', title=''),
                y=alt.Y('Variável 2:N', title=''),
                color=alt.Color('Correlação:Q',
                    scale=alt.Scale(domain=(-1, 1), range=['darkred', 'white', 'darkblue']),
                    legend=alt.Legend(title="Correlação")
                ),
                tooltip=['Variável 1', 'Variável 2', alt.Tooltip('Correlação', format='.3f')]
            ).properties(
                width=400,
                height=400,
                title="Heatmap de Correlação"
            )

            st.altair_chart(heatmap, width='stretch')

            # Tabela de Correlação
            st.subheader("Tabela de Correlação")
            st.dataframe(
                corr_matrix.style.background_gradient(cmap='RdYlBu', axis=None, vmin=-1, vmax=1)
                .format("{:.3f}"),
                width='stretch'
            )

            # Correlações Mais Fortes
            st.subheader("Correlações Mais Fortes")
            # Obter triângulo superior da matriz de correlação
            upper = corr_matrix.where(np.triu(np.ones_like(corr_matrix), k=1).astype(bool))
            top_corr = upper.stack().sort_values(ascending=False).head(10)

            if len(top_corr) > 0:
                top_corr_df = pd.DataFrame({
                    'Variável 1': [idx[0] for idx in top_corr.index],
                    'Variável 2': [idx[1] for idx in top_corr.index],
                    'Correlação': top_corr.values
                })

                st.dataframe(
                    top_corr_df.style.background_gradient(subset=['Correlação'], cmap='RdYlBu', vmin=-1, vmax=1)
                    .format({'Correlação': '{:.3f}'}),
                    width='stretch'
                )

            # Seção de Scatter Plot
            st.subheader("Scatter Plot Interativo")
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                x_col = st.selectbox("Eixo X:", numeric_columns, key="scatter_x")
            with col2:
                y_col = st.selectbox("Eixo Y:", numeric_columns, key="scatter_y")
            with col3:
                color_by = st.selectbox("Colorir por:", ["Nenhum"] + list(categorical_cols), key="scatter_color")

            if x_col and y_col and x_col != y_col:
                # Criar dados de dispersão com nomes de colunas únicos
                scatter_data = df_filtered[[x_col, y_col]].dropna().copy()
                if len(scatter_data) > 0:
                    if color_by != "Nenhum" and color_by in df_filtered.columns and color_by not in [x_col, y_col]:
                        # Adição segura da coluna de cor
                        color_values = df_filtered.loc[scatter_data.index, color_by]
                        scatter_data = pd.concat([scatter_data, color_values.rename(color_by)], axis=1)

                        scatter = alt.Chart(scatter_data).mark_circle(size=60).encode(
                            x=alt.X(f'{x_col}:Q', title=x_col),
                            y=alt.Y(f'{y_col}:Q', title=y_col),
                            color=alt.Color(f'{color_by}:N', title=color_by),
                            tooltip=[x_col, y_col, color_by]
                        ).properties(height=400)
                    else:
                        scatter = alt.Chart(scatter_data).mark_circle(size=60, color='coral').encode(
                            x=alt.X(f'{x_col}:Q', title=x_col),
                            y=alt.Y(f'{y_col}:Q', title=y_col),
                            tooltip=[x_col, y_col]
                        ).properties(height=400)

                    st.altair_chart(scatter, width='stretch')

                    # Estatísticas detalhadas de correlação
                    corr = scatter_data[x_col].corr(scatter_data[y_col])
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Correlação Pearson", ".3f")
                    with col2:
                        st.metric("R²", ".3f")
                    with col3:
                        st.metric("Pontos", len(scatter_data))
                    with col4:
                        # Interpretar força da correlação
                        strength = "Forte" if abs(corr) > 0.7 else "Moderada" if abs(corr) > 0.3 else "Fraca"
                        direction = "Positiva" if corr > 0 else "Negativa" if corr < 0 else "Nenhuma"
                        st.metric("Força", f"{strength} ({direction})")
                else:
                    st.warning("Não há dados suficientes para criar o scatter plot.")
            else:
                st.info("Selecione variáveis diferentes para X e Y.")
        else:
            st.info("São necessárias pelo menos 2 colunas numéricas para análise de correlação.")

    with tab5:
        st.markdown("**📅 Temporal** - Evolução ao longo do tempo")

        numeric_columns = df_filtered.select_dtypes(include=['number']).columns

        # Só permite análise temporal se 'Ano' estiver nas colunas selecionadas
        if 'Ano' in df_filtered.columns and len(numeric_columns) > 0:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                ts_col = st.selectbox("Coluna numérica:", numeric_columns, key="ts_col")
            with col2:
                agg_func = st.selectbox("Agregação:", ["Soma", "Média", "Contagem"], key="ts_agg")
            with col3:
                chart_type = st.selectbox("Tipo:", ["Linha", "Área", "Barra"], key="ts_type")

            if ts_col:
                    # Agregar dados por ano
                    if agg_func == "Soma":
                        ts_data = df_filtered.groupby('Ano')[ts_col].sum().reset_index()
                    elif agg_func == "Média":
                        ts_data = df_filtered.groupby('Ano')[ts_col].mean().reset_index()
                    else:  # Contagem
                        ts_data = df_filtered.groupby('Ano')[ts_col].count().reset_index()

                    # Criar tipo de gráfico apropriado
                    if chart_type == "Linha":
                        ts_chart = alt.Chart(ts_data).mark_line(
                            point=True,
                            color='steelblue',
                            strokeWidth=3
                        ).encode(
                            x=alt.X('Ano:O', title='Ano'),
                            y=alt.Y(f'{ts_col}:Q', title=f'{agg_func} de {ts_col}'),
                            tooltip=['Ano', alt.Tooltip(ts_col, format='.2f')]
                        ).properties(height=350)
                    elif chart_type == "Área":
                        ts_chart = alt.Chart(ts_data).mark_area(
                            color='lightblue',
                            opacity=0.7
                        ).encode(
                            x=alt.X('Ano:O', title='Ano'),
                            y=alt.Y(f'{ts_col}:Q', title=f'{agg_func} de {ts_col}'),
                            tooltip=['Ano', alt.Tooltip(ts_col, format='.2f')]
                        ).properties(height=350)
                    else:  # Barra
                        ts_chart = alt.Chart(ts_data).mark_bar(
                            color='steelblue',
                            opacity=0.8
                        ).encode(
                            x=alt.X('Ano:O', title='Ano'),
                            y=alt.Y(f'{ts_col}:Q', title=f'{agg_func} de {ts_col}'),
                            tooltip=['Ano', alt.Tooltip(ts_col, format='.2f')]
                        ).properties(height=350)

                    st.altair_chart(ts_chart, width='stretch')

                    # Análise de tendência aprimorada
                    if len(ts_data) > 1:
                        # Calcular métricas de tendência
                        first_val = ts_data[ts_col].iloc[0]
                        last_val = ts_data[ts_col].iloc[-1]
                        change_pct = ((last_val - first_val) / first_val) * 100 if first_val != 0 else 0

                        # Calcular volatilidade (coeficiente de variação)
                        mean_val = ts_data[ts_col].mean()
                        std_val = ts_data[ts_col].std()
                        volatility = (std_val / mean_val * 100) if mean_val != 0 else 0

                        # Exibir métricas aprimoradas
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            trend = "📈 Crescimento" if change_pct > 0 else "📉 Declínio" if change_pct < 0 else "➡️ Estável"
                            st.metric("Tendência Geral", trend)
                        with col2:
                            st.metric(f"Variação Total ({ts_data['Ano'].iloc[0]}→{ts_data['Ano'].iloc[-1]})", f"{change_pct:.1f}%")
                        with col3:
                            st.metric("Valor Máximo", f"{ts_data[ts_col].max():.2f}")
                        with col4:
                            st.metric("Volatilidade", f"{volatility:.1f}%")

                        # Variações ano a ano
                        if len(ts_data) > 2:
                            st.subheader("📊 Variações Ano a Ano")
                            yoy_changes = []
                            for i in range(1, len(ts_data)):
                                prev_val = ts_data[ts_col].iloc[i-1]
                                curr_val = ts_data[ts_col].iloc[i]
                                if prev_val != 0:
                                    yoy_change = ((curr_val - prev_val) / prev_val) * 100
                                    yoy_changes.append({
                                        'Período': f"{ts_data['Ano'].iloc[i-1]}→{ts_data['Ano'].iloc[i]}",
                                        'Variação': yoy_change
                                    })

                            if yoy_changes:
                                yoy_df = pd.DataFrame(yoy_changes)
                                yoy_chart = alt.Chart(yoy_df).mark_bar().encode(
                                    x='Período:O',
                                    y='Variação:Q',
                                    color=alt.condition(
                                        alt.datum.Variação > 0,
                                        alt.value('green'),
                                        alt.value('red')
                                    ),
                                    tooltip=['Período', alt.Tooltip('Variação', format='.1f')]
                                ).properties(height=250)

                                st.altair_chart(yoy_chart, width='stretch')

                                # Resumo das mudanças
                                positive_changes = sum(1 for change in yoy_changes if change['Variação'] > 0)
                                total_changes = len(yoy_changes)
                                consistency = (positive_changes / total_changes) * 100 if total_changes > 0 else 0

                                st.metric("Consistência de Crescimento", ".0f")

                    # Tabela de dados com formatação aprimorada
                    st.subheader("📋 Dados Temporais Detalhados")
                    display_ts = ts_data.copy()
                    display_ts[ts_col] = display_ts[ts_col].round(2)

                    # Adicionar coluna de variação percentual
                    if len(display_ts) > 1:
                        display_ts['Variação %'] = display_ts[ts_col].pct_change() * 100
                        display_ts['Variação %'] = display_ts['Variação %'].round(1)

                    st.dataframe(
                        display_ts.style.background_gradient(subset=[ts_col], cmap='YlGnBu')
                        .format({ts_col: '{:,.2f}', 'Variação %': '{:+.1f}%'}),
                        width='stretch'
                    )
            else:
                st.info("Nenhuma coluna numérica disponível para análise temporal.")
        else:
            st.info("Coluna 'Ano' não encontrada para análise temporal.")

    # Baixar dados filtrados
    csv = df_filtered.to_csv(index=False)
    st.download_button(
        label="📥 Baixar Dados Filtrados como CSV",
        data=csv,
        file_name=f"{selected_dataset.replace(' ', '_').lower()}_filtrados.csv",
        mime="text/csv"
    )

    # Seção de Consulta SQL (manter para usuários avançados)
    st.header("🔍 Interface Avançada de Consulta SQL")
    with st.expander("Consulta SQL (para usuários avançados)"):
        st.markdown("Use SQL para consultar seus dados. Tabelas disponíveis:")
        table_list = [file.replace('.csv', '').replace('-', '_').replace(' ', '_').lower() for file in datasets.values() if load_csv(file) is not None]
        st.code(", ".join(table_list), language="sql")

        query = st.text_area("Digite sua consulta SQL:", value=f"SELECT * FROM {table_name} LIMIT 10;", height=100)

        if st.button("Executar Consulta SQL"):
            try:
                result = conn.execute(query).fetchdf()
                st.success(f"Consulta executada com sucesso! Retornou {len(result)} linhas.")
                st.dataframe(result, width='stretch')

                # Botão de download
                csv = result.to_csv(index=False)
                st.download_button(
                    label="📥 Baixar Resultados SQL como CSV",
                    data=csv,
                    file_name="resultados_sql.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"Erro ao executar consulta: {str(e)}")

else:
    st.error(f"Conjunto de dados '{selected_dataset}' não encontrado. Execute o script de coleta primeiro.")
