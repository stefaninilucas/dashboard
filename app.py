from etl_data import etl_data
from dashboard.filtros import filtro
from dashboard.metricas import metrica
from dashboard.tabelas import tabela
from dashboard.markdown import markdown
from dashboard.graficos import grafico_barra_emp
import streamlit as st
import pandas as pd

produtos = ['Chocolate', 'Biscoito', 'Snack']
tipos = ['Meta', 'Vendas']
meses = [1, 2, 3]
cores_por_produto={
    produtos[0]: '#502172',
    produtos[1]: '#0071b8',
    produtos[2]: '#00b2c4'
}

df = etl_data(produtos, tipos, meses)
st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

# banner
st.markdown(
    """
    <div style="background-color:#502172;text-align:center">
        <img src="https://raw.githubusercontent.com/stefaninilucas/dashboard/refs/heads/branch1/image/banner.png" style="width:75%;height:auto;">
    </div><br><br>
    """,
    unsafe_allow_html=True
)

# filtro
df_filtrado = filtro(df)

# metricas
total_vendedores = len(df)
total_vendas = [pd.to_numeric(df[(produto,"Vendas Total")]).sum() for produto in produtos]

col1, col2, col3, col4 = st.columns(4)

with col1:
    metrica(df, "Total de Vendedores", total_vendedores)

with col2:
    metrica(df, f"Total de Vendas {produtos[0]}", round(total_vendas[0],1))

with col3:
    metrica(df, f"Total de Vendas {produtos[1]}", round(total_vendas[1],1))

with col4:
    metrica(df, f"Total de Vendas {produtos[2]}", round(total_vendas[2],1))


# tabela
tabela1 = tabela(df_filtrado,"Ranking Geral")

# markdown
markdown1 = markdown("🛈 Critérios de Desempate: 1° Pontos Chocolate | 2° Pontos Biscoito | 3° Pontos Snack<br><br>", 12)
markdown2 = markdown("""🛈 Legenda:                                
                        **M1, M2, M3**: Metas mensais (meses 1, 2 e 3)  
                        | **V1, V2, V3**: Vendas mensais (meses 1, 2 e 3)  
                        | **Meta Total**: Soma das metas dos 3 meses  
                        | **Vendas Total**: Soma das vendas dos 3 meses  
                        | **Resultado**: Vendas ÷ Meta  
                        | **Pontos**: Resultado × 10 (arredondado para baixo)  
                        | **Pontuação**: Soma dos pontos dos 3 produtos<br><br><br><br>""", 12)


# gráfico de barras empilhadas

# cria dataframe exclusivo para o grafico
pontos_cols = [(produto, "Pontos") for produto in produtos]
colunas = [("Vendedor", ""), ("Posição", "")] + pontos_cols
df_grafico = df[colunas].copy()
df_grafico.columns = ['Vendedor', 'Posição', 'Chocolate', 'Biscoito', 'Snack']

df_grafico['Posição_Vendedor'] = df_grafico['Posição'].astype(str) + " - " + df['Vendedor'] # Cria coluna para o eixo Y com "Posição - Vendedor"

grafico1 = grafico_barra_emp(df_grafico,"Gráfico - Ranking de Pontuação",produtos,'Posição_Vendedor', cores_por_produto)