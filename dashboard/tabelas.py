import streamlit as st

def tabela(df, titulo):
    
    st.subheader(titulo)
    st.dataframe(df, use_container_width=True, hide_index=True)
