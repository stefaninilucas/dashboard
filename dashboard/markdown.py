import streamlit as st

def markdown(texto, font_size):
    st.markdown(f"""
    <div style="font-size:{font_size}px;">            
    {texto}
    """, unsafe_allow_html=True)

