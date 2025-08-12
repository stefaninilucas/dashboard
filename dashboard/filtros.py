import streamlit as st

def filtro(df):

    

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

    return df_filtrado