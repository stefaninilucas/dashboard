

import streamlit as st

def metrica(df, titulo, valor):
    total_vendedores = len(df)
    st.metric(titulo, valor)