def publicar(df):
    import streamlit as st
    import plotly.express as px

    st.set_page_config(page_title="Dashboard", layout="wide")
    st.title("Campanha de Incentivos 2025")

    total_vendedores = len(df)
    st.metric("Total de Vendedores", total_vendedores)

    vendedores_disponiveis = df[("Vendedor", "")].unique().tolist()
    vendedores_disponiveis.sort()

    st.sidebar.markdown("### Filtrar Vendedores")

    # Botão para selecionar/deselecionar todos
    if 'selecionar_todos' not in st.session_state:
        st.session_state.selecionar_todos = True

    def toggle_selecionar_todos():
        st.session_state.selecionar_todos = not st.session_state.selecionar_todos

    st.sidebar.button(
        "Selecionar/Deselecionar Todos",
        on_click=toggle_selecionar_todos
    )

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

    # Tabela
    st.subheader("Tabela Ranking")
    st.dataframe(df_filtrado, use_container_width=True, hide_index=True)

    # Legenda
    st.markdown("""
    ### 🛈 Legenda
    - **M1, M2, M3**: Metas mensais (meses 1, 2 e 3)  
    - **V1, V2, V3**: Vendas mensais (meses 1, 2 e 3)  
    - **Meta Total**: Soma das metas dos 3 meses  
    - **Vendas Total**: Soma das vendas dos 3 meses  
    - **Resultado**: Vendas ÷ Meta  
    - **Pontos**: Resultado × 10 (arredondado para baixo)  
    - **Pontuação**: Soma dos pontos dos 3 produtos  
    """)

    # Gráfico de barras empilhadas (mesmo código que antes)
    st.subheader("Ranking de Pontuação - Pontos por Produto")

    pontos_cols = [(produto, "Pontos") for produto in ['Chocolate', 'Biscoito', 'Snack']]
    df_grafico = df_filtrado[[("Vendedor", "")] + pontos_cols].copy()
    df_grafico.columns = ['Vendedor', 'Chocolate', 'Biscoito', 'Snack']
    df_grafico = df_grafico.sort_values(by=['Chocolate', 'Biscoito', 'Snack'], ascending=True)

    fig = px.bar(
        df_grafico,
        y='Vendedor',
        x=['Chocolate', 'Biscoito', 'Snack'],
        orientation='h',
        text_auto=True,
        color_discrete_map={
            'Chocolate': '#7b3f00',
            'Biscoito': '#f4c430',
            'Snack': '#2e8b57'
        },
        height=600,
    )

    fig.update_layout(
        xaxis_title="Pontos",
        yaxis_title="Vendedor",
        barmode='stack',
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=14),
    )

    st.plotly_chart(fig, use_container_width=True)


