def publicar(df):
    import streamlit as st
    import plotly.express as px

    st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
    st.title("Campanha de Incentivos 2025")

    # filtros
    st.sidebar.header("🔍 Filtros")

    # Botão para selecionar/deselecionar todos
    if 'selecionar_todos' not in st.session_state:
        st.session_state.selecionar_todos = True

    def toggle_selecionar_todos():
        st.session_state.selecionar_todos = not st.session_state.selecionar_todos

    st.sidebar.button(
        "Selecionar/Deselecionar Todos",
        on_click=toggle_selecionar_todos
    )

    vendedores_disponiveis = df[("Vendedor", "")].unique().tolist()
    vendedores_disponiveis.sort()

    # Criar checkboxes para cada vendedor
    vendedores_selecionados = []
    for vendedor in vendedores_disponiveis:
        default_checked = st.session_state.selecionar_todos
        checked = st.sidebar.checkbox(vendedor, value=default_checked, key=f"chk_{vendedor}")
        if checked:
            vendedores_selecionados.append(vendedor)

    if not vendedores_selecionados:
        st.sidebar.warning("Selecione pelo menos um vendedor para exibir os dados.")
        # Evitar erro ao filtrar com lista vazia
        vendedores_selecionados = vendedores_disponiveis.copy()

    df_filtrado = df[df[("Vendedor", "")].isin(vendedores_selecionados)]

    # metricas
    total_vendedores = len(df)
    st.metric("Total de Vendedores", total_vendedores)

    # Tabela
    st.subheader("Ranking Geral")
    st.dataframe(df_filtrado, use_container_width=True, hide_index=True)

    # Legenda

    st.markdown("""
    <div style="font-size:16px;">            
    🛈 Critérios de Desempate:
    1° Pontos Chocolate | 2° Pontos Biscoito | 3° Pontos Snack
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:16px;">            
    🛈 Legenda:
    <br>            
    **M1, M2, M3**: Metas mensais (meses 1, 2 e 3)  
    | **V1, V2, V3**: Vendas mensais (meses 1, 2 e 3)  
    | **Meta Total**: Soma das metas dos 3 meses  
    | **Vendas Total**: Soma das vendas dos 3 meses  
    | **Resultado**: Vendas ÷ Meta  
    | **Pontos**: Resultado × 10 (arredondado para baixo)  
    | **Pontuação**: Soma dos pontos dos 3 produtos
    <br><br><br><br><br><br>
    """, unsafe_allow_html=True)

    # Gráfico de barras empilhadas (mesmo código que antes)
    st.subheader("Gráfico - Ranking de Pontuação")

    pontos_cols = [(produto, "Pontos") for produto in ['Chocolate', 'Biscoito', 'Snack']]
    colunas = [("Vendedor", ""), ("Posição", "")] + pontos_cols
    df_grafico = df_filtrado[colunas].copy()
    df_grafico.columns = ['Vendedor', 'Posição', 'Chocolate', 'Biscoito', 'Snack']

    # Ordena por posição
    df_grafico = df_grafico.sort_values(by='Posição', ascending=False)

    # Soma total dos pontos
    df_grafico['Total'] = df_grafico[['Chocolate', 'Biscoito', 'Snack']].sum(axis=1)

    # Cria coluna para o eixo Y com "Posição - Vendedor"
    df_grafico['Posição_Vendedor'] = df_grafico['Posição'].astype(str) + " - " + df_grafico['Vendedor']

    fig = px.bar(
        df_grafico,
        y='Posição_Vendedor',
        x=['Chocolate', 'Biscoito', 'Snack'],
        orientation='h',
        text_auto=True,
        color_discrete_map={
            'Chocolate': '#502172',
            'Biscoito': '#0071b8',
            'Snack': '#00b2c4'
        },
        height=800,
        labels={"variable": ""}
    )

    # Adiciona total à direita das barras como inteiro
    for i, row in df_grafico.iterrows():
        fig.add_annotation(
            x=row['Total'] + 1,
            y=row['Posição_Vendedor'],
            text=str(int(row['Total'])),
            showarrow=False,
            font=dict(size=16, color='black'),
            xanchor='left',
            yanchor='middle'
        )

    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        barmode='stack',
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=14),
        margin=dict(r=100),
        yaxis=dict(tickfont=dict(size=16))
    )

    # Esconde os rótulos do eixo X
    fig.update_xaxes(showticklabels=False)

    st.plotly_chart(fig, use_container_width=True)

    