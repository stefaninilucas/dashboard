from etl_data import etl_data
from dashboard.filtros import filtro
from dashboard.metricas import metrica
from dashboard.tabelas import tabela
from dashboard.markdown import markdown
from dashboard.graficos import grafico_barra_emp
import streamlit as st
import plotly.express as px

df = etl_data()
st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
st.title("Campanha de Incentivos 2025")

# filtro
df_filtrado = filtro(df)

# metrica
total_vendedores = len(df)
metrica1 = metrica(df, "Total de Vendedores", total_vendedores)

# tabela
tabela1 = tabela(df_filtrado,"Ranking Geral")


# markdown
markdown1 = markdown("🛈 Critérios de Desempate: 1° Pontos Chocolate | 2° Pontos Biscoito | 3° Pontos Snack<br><br>", 16)
markdown2 = markdown("""🛈 Legenda:                                
                        **M1, M2, M3**: Metas mensais (meses 1, 2 e 3)  
                        | **V1, V2, V3**: Vendas mensais (meses 1, 2 e 3)  
                        | **Meta Total**: Soma das metas dos 3 meses  
                        | **Vendas Total**: Soma das vendas dos 3 meses  
                        | **Resultado**: Vendas ÷ Meta  
                        | **Pontos**: Resultado × 10 (arredondado para baixo)  
                        | **Pontuação**:' Soma dos pontos dos 3 produtos<br><br><br><br>""", 16)


# gráfico de barras empilhadas

grafico1 = grafico_barra_emp(df_filtrado,"Gráfico - Ranking de Pontuação")

