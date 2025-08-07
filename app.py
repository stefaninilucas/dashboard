import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Título do app
st.set_page_config(page_title="Dashboard", layout="wide")
st.title("Campanha de Incentivos 2025")

# Carregar a base de dados
df = pd.read_excel("base_dados.xlsx")

# Aplicar mecânicas na base de Dados

#'criar um dataframe com os vendedores únicos'
df_vendedores = df['vendedor'].drop_duplicates()

#'criar dataframes para cada produto, mes e tipo de dado (meta e vendas)'
df_chocolate_meta1 = df[(df['produto'] == 'Chocolate') & (df['mes'] == 1)][['vendedor', 'meta']]
df_chocolate_meta1.rename(columns={'meta': 'Chocolate Meta 1'}, inplace=True)

df_chocolate_meta2 = df[df['produto'] == 'Chocolate'][df['mes'] == 2][['vendedor', 'meta']]
df_chocolate_meta2.rename(columns={'meta': 'Chocolate Meta 2'}, inplace=True)

df_chocolate_meta3 = df[df['produto'] == 'Chocolate'][df['mes'] == 3][['vendedor', 'meta']]
df_chocolate_meta3.rename(columns={'meta': 'Chocolate Meta 3'}, inplace=True)

df_chocolate_vendas1 = df[df['produto'] == 'Chocolate'][df['mes'] == 1][['vendedor', 'vendas']]
df_chocolate_vendas1.rename(columns={'vendas': 'Chocolate Vendas 1'}, inplace=True)

df_chocolate_vendas2 = df[df['produto'] == 'Chocolate'][df['mes'] == 2][['vendedor', 'vendas']]
df_chocolate_vendas2.rename(columns={'vendas': 'Chocolate Vendas 2'}, inplace=True)

df_chocolate_vendas3 = df[df['produto'] == 'Chocolate'][df['mes'] == 3][['vendedor', 'vendas']]
df_chocolate_vendas3.rename(columns={'vendas': 'Chocolate Vendas 3'}, inplace=True)

df_biscoito_meta1 = df[df['produto'] == 'Biscoito'][df['mes'] == 1][['vendedor', 'meta']]
df_biscoito_meta1.rename(columns={'meta': 'Biscoito Meta 1'}, inplace=True)

df_biscoito_meta2 = df[df['produto'] == 'Biscoito'][df['mes'] == 2][['vendedor', 'meta']]
df_biscoito_meta2.rename(columns={'meta': 'Biscoito Meta 2'}, inplace=True)

df_biscoito_meta3 = df[df['produto'] == 'Biscoito'][df['mes'] == 3][['vendedor', 'meta']]
df_biscoito_meta3.rename(columns={'meta': 'Biscoito Meta 3'}, inplace=True)

df_biscoito_vendas1 = df[df['produto'] == 'Biscoito'][df['mes'] == 1][['vendedor', 'vendas']]
df_biscoito_vendas1.rename(columns={'vendas': 'Biscoito Vendas 1'}, inplace=True)

df_biscoito_vendas2 = df[df['produto'] == 'Biscoito'][df['mes'] == 2][['vendedor', 'vendas']]
df_biscoito_vendas2.rename(columns={'vendas': 'Biscoito Vendas 2'}, inplace=True)

df_biscoito_vendas3 = df[df['produto'] == 'Biscoito'][df['mes'] == 3][['vendedor', 'vendas']]
df_biscoito_vendas3.rename(columns={'vendas': 'Biscoito Vendas 3'}, inplace=True)

df_snack_meta1 = df[df['produto'] == 'Snack'][df['mes'] == 1][['vendedor', 'meta']]
df_snack_meta1.rename(columns={'meta': 'Snack Meta 1'}, inplace=True)

df_snack_meta2 = df[df['produto'] == 'Snack'][df['mes'] == 2][['vendedor', 'meta']]
df_snack_meta2.rename(columns={'meta': 'Snack Meta 2'}, inplace=True)

df_snack_meta3 = df[df['produto'] == 'Snack'][df['mes'] == 3][['vendedor', 'meta']]
df_snack_meta3.rename(columns={'meta': 'Snack Meta 3'}, inplace=True)

df_snack_vendas1 = df[df['produto'] == 'Snack'][df['mes'] == 1][['vendedor', 'vendas']]
df_snack_vendas1.rename(columns={'vendas': 'Snack Vendas 1'}, inplace=True)

df_snack_vendas2 = df[df['produto'] == 'Snack'][df['mes'] == 2][['vendedor', 'vendas']]
df_snack_vendas2.rename(columns={'vendas': 'Snack Vendas 2'}, inplace=True)

df_snack_vendas3 = df[df['produto'] == 'Snack'][df['mes'] == 3][['vendedor', 'vendas']]
df_snack_vendas3.rename(columns={'vendas': 'Snack Vendas 3'}, inplace=True)


#'criar um dataframe final com todos os dados'
df_ranking = pd.merge(df_vendedores, df_chocolate_meta1, on='vendedor')
df_ranking = pd.merge(df_ranking, df_chocolate_meta2, on='vendedor')
df_ranking = pd.merge(df_ranking, df_chocolate_meta3, on='vendedor')
df_ranking['Chocolate Meta Total'] = df_ranking['Chocolate Meta 1'] + df_ranking['Chocolate Meta 2'] + df_ranking['Chocolate Meta 3']
df_ranking = pd.merge(df_ranking, df_chocolate_vendas1, on='vendedor')
df_ranking = pd.merge(df_ranking, df_chocolate_vendas2, on='vendedor')
df_ranking = pd.merge(df_ranking, df_chocolate_vendas3, on='vendedor')
df_ranking['Chocolate Vendas Total'] = df_ranking['Chocolate Vendas 1'] + df_ranking['Chocolate Vendas 2'] + df_ranking['Chocolate Vendas 3']
df_ranking['Chocolate Resultado'] = df_ranking['Chocolate Vendas Total'] / df_ranking['Chocolate Meta Total']
df_ranking['Chocolate Pontos'] = np.floor(df_ranking['Chocolate Resultado'] * 10)
df_ranking['Chocolate Resultado'] = df_ranking['Chocolate Resultado'].map('{:.2f}%'.format)


df_ranking = pd.merge(df_ranking, df_biscoito_meta1, on='vendedor')
df_ranking = pd.merge(df_ranking, df_biscoito_meta2, on='vendedor')
df_ranking = pd.merge(df_ranking, df_biscoito_meta3, on='vendedor')
df_ranking['Biscoito Meta Total'] = df_ranking['Biscoito Meta 1'] + df_ranking['Biscoito Meta 2'] + df_ranking['Biscoito Meta 3']
df_ranking = pd.merge(df_ranking, df_biscoito_vendas1, on='vendedor')
df_ranking = pd.merge(df_ranking, df_biscoito_vendas2, on='vendedor')
df_ranking = pd.merge(df_ranking, df_biscoito_vendas3, on='vendedor')
df_ranking['Biscoito Vendas Total'] = df_ranking['Biscoito Vendas 1'] + df_ranking['Biscoito Vendas 2'] + df_ranking['Biscoito Vendas 3']
df_ranking['Biscoito Resultado'] = df_ranking['Biscoito Vendas Total'] / df_ranking['Biscoito Meta Total']
df_ranking['Biscoito Pontos'] = np.floor(df_ranking['Biscoito Resultado'] * 10)
df_ranking['Biscoito Resultado'] = df_ranking['Biscoito Resultado'].map('{:.2f}%'.format)

df_ranking = pd.merge(df_ranking, df_snack_meta1, on='vendedor')
df_ranking = pd.merge(df_ranking, df_snack_meta2, on='vendedor')
df_ranking = pd.merge(df_ranking, df_snack_meta3, on='vendedor')
df_ranking['Snack Meta Total'] = df_ranking['Snack Meta 1'] + df_ranking['Snack Meta 2'] + df_ranking['Snack Meta 3']
df_ranking = pd.merge(df_ranking, df_snack_vendas1, on='vendedor')
df_ranking = pd.merge(df_ranking, df_snack_vendas2, on='vendedor')
df_ranking = pd.merge(df_ranking, df_snack_vendas3, on='vendedor')
df_ranking['Snack Vendas Total'] = df_ranking['Snack Vendas 1'] + df_ranking['Snack Vendas 2'] + df_ranking['Snack Vendas 3']
df_ranking['Snack Resultado'] = df_ranking['Snack Vendas Total'] / df_ranking['Snack Meta Total']
df_ranking['Snack Pontos'] = np.floor(df_ranking['Snack Resultado'] * 10)
df_ranking['Snack Resultado'] = df_ranking['Snack Resultado'].map('{:.2f}%'.format)

df_ranking['Total Pontos'] = df_ranking['Chocolate Pontos'] + df_ranking['Biscoito Pontos'] + df_ranking['Snack Pontos']

df_ranking.sort_values(by=['Total Pontos','Chocolate Pontos','Biscoito Pontos','Snack Pontos'], ascending=[False, False, False, False], inplace=True)
df_ranking.reset_index(drop=True, inplace=True)
df_ranking.insert(0, 'posição', df_ranking.index + 1)
df_ranking.index = [''] * len(df_ranking)


# Mostrar os dados
st.subheader("Tabela - Ranking dos Vendedores")
st.dataframe(df_ranking, use_container_width=True, hide_index=True)

# #Filtragem (automática por colunas categóricas)
# st.sidebar.header("🎯 Filtros")
# colunas_categoricas = df_ranking.select_dtypes(include=["object", "category"]).columns

# filtros = {}
# for col in colunas_categoricas:
#     opcoes = df_ranking[col].dropna().unique()
#     selecionados = st.sidebar.multiselect(f"Filtrar por {col}", opcoes, default=opcoes)
#     filtros[col] = selecionados

# # Aplicar filtros
# df_filtrado = df_ranking.copy()
# for col, valores in filtros.items():
#     df_filtrado = df_filtrado[df_filtrado[col].isin(valores)]

filtros = {}
st.sidebar.header("Filtros")
opcoes = df_ranking['vendedor'].dropna().unique()
selecionados = st.sidebar.multiselect("Filtrar por Vendedor", opcoes, default=opcoes)
filtros['vendedor'] = selecionados

df_filtrado = df_ranking.copy()
df_filtrado = df_filtrado[df_filtrado['vendedor'].isin(filtros['vendedor'])]


# Gráfico de exemplo (você pode personalizar depois)
# st.subheader("📊 Gráfico de exemplo")
# coluna_num = st.selectbox("Selecione a coluna numérica para visualizar:", df_filtrado.select_dtypes(include=["number"]).columns)
# coluna_cat = st.selectbox("Agrupar por:", colunas_categoricas)

# Plotar
# fig, ax = plt.subplots()
# df_filtrado.groupby(coluna_cat)[coluna_num].mean().plot(kind="bar", ax=ax, color="skyblue")
# ax.set_ylabel(f"Média de {coluna_num}")
# st.pyplot(fig)


st.subheader("Gráfico - Ranking dos Vendedores")
fig, ax = plt.subplots(figsize=(10, 10))
# df_filtrado.plot(kind='bar', x='vendedor', y=['Chocolate Pontos', 'Biscoito Pontos', 'Snack Pontos'], ax=ax, color=['#FF6347', '#FFD700', '#32CD32'])

df_filtrado.plot(
    kind='barh',
    x='vendedor',
    y=['Chocolate Pontos', 'Biscoito Pontos', 'Snack Pontos'],
    ax=ax,
    stacked=True,
    color=["#9D47FF", "#2200FF", "#32A1CD"],
)

ax.set_xlabel("Total de Pontos")
ax.set_ylabel("Vendedor")
ax.set_title("Pontuação por Categoria - Gráfico Empilhado")
ax.invert_yaxis()
plt.tight_layout()
st.pyplot(fig)