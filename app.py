import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Função para criar colunas por produto, tipo e mês
def criar_coluna(df, produto, tipo, mes):
    nome_coluna = f"{produto} {tipo} {mes}"
    return df[(df['produto'] == produto) & (df['mes'] == mes)][['vendedor', tipo.lower()]].rename(columns={tipo.lower(): nome_coluna})



# Carregar base
df = pd.read_excel("base_dados.xlsx")

# Produtos, tipos e meses
produtos = ['Chocolate', 'Biscoito', 'Snack']
tipos = ['Meta', 'Vendas']
meses = ['1', '2', '3']

# Inicia ranking com vendedores únicos
df_ranking = df[['vendedor']].drop_duplicates().reset_index(drop=True)

# Adiciona as colunas de metas e vendas de cada produto por mês no ranking
for produto in produtos:
    for tipo in tipos:
        for mes in meses:
            col_df = criar_coluna(df, produto, tipo, int(mes))
            df_ranking = df_ranking.merge(col_df, on='vendedor', how='left')

    # Totais
    metas_cols = [f"{produto} Meta {m}" for m in meses]
    vendas_cols = [f"{produto} Vendas {m}" for m in meses]

    df_ranking[f"{produto} Meta Total"] = df_ranking[metas_cols].sum(axis=1)
    df_ranking[f"{produto} Vendas Total"] = df_ranking[vendas_cols].sum(axis=1)

    # Resultado numérico e formatado
    df_ranking[f"{produto} Resultado"] = df_ranking[f"{produto} Vendas Total"] / df_ranking[f"{produto} Meta Total"]
    df_ranking[f"{produto} Pontos"] = np.floor(df_ranking[f"{produto} Resultado"] * 10)
    df_ranking[f"{produto} Resultado Formatado"] = df_ranking[f"{produto} Resultado"].map('{:.2%}'.format)

# Pontuação total
df_ranking['Total Pontos'] = df_ranking[[f"{p} Pontos" for p in produtos]].sum(axis=1)

# Ordenar e numerar
df_ranking.sort_values(by=['Total Pontos'] + [f"{p} Pontos" for p in produtos], ascending=False, inplace=True)
df_ranking.reset_index(drop=True, inplace=True)
df_ranking.insert(0, 'posição', df_ranking.index + 1)

# Criar estrutura de MultiIndex para exibição
multi_cols = [('', '', 'Posição'), ('', '', 'Vendedor')]
dados = [df_ranking['posição'], df_ranking['vendedor']]

for produto in produtos:
    for tipo in ['Meta', 'Vendas']:
        for mes in ['1', '2', '3', 'Total']:
            nome_col = f"{produto} {tipo} {mes}"
            if nome_col in df_ranking.columns:
                multi_cols.append((produto, tipo, mes))
                dados.append(df_ranking[nome_col])
    multi_cols.append((produto, 'Pontos', ''))
    dados.append(df_ranking[f"{produto} Pontos"])

multi_cols.append(('Total', 'Pontos', ''))
dados.append(df_ranking['Total Pontos'])

multi_index = pd.MultiIndex.from_tuples(multi_cols)
df_multi = pd.DataFrame(list(zip(*dados)), columns=multi_index)


# Configuração da página
st.set_page_config(page_title="Dashboard", layout="wide")
st.title("Campanha de Incentivos 2025")

# Filtros
st.sidebar.header("Filtros")
opcoes = df_ranking['vendedor'].dropna().unique()
selecionados = st.sidebar.multiselect("Filtrar por Vendedor", opcoes, default=opcoes)

df_multi_filtrado = df_multi[df_multi[('', '', 'Vendedor')].isin(selecionados)]

# Exibir tabela com cabeçalho mesclado
st.subheader("📊 Tabela com Cabeçalhos Agrupados")
st.dataframe(df_multi_filtrado, use_container_width=True)

# Gráfico de Pontuação por Categoria
st.subheader("📈 Gráfico - Ranking dos Vendedores")

# Montar DataFrame para o gráfico
df_grafico = df_ranking[df_ranking['vendedor'].isin(selecionados)][['vendedor'] + [f"{p} Pontos" for p in produtos]]

fig, ax = plt.subplots(figsize=(10, 10))
df_grafico.plot(
    kind='barh',
    x='vendedor',
    y=[f"{p} Pontos" for p in produtos],
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
