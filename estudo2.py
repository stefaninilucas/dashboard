import numpy as np
import pandas as pd

produtos = ['chocolate', 'biscoito', 'snack']
tipos = ['meta', 'vendas']

df_base = pd.read_excel("base_dados.xlsx")

df_base['produto'] = df_base['produto'].str.lower()

df_base_pivot = df_base.pivot_table(index='vendedor', columns=['produto', 'mes'], values=['meta', 'vendas'], aggfunc='sum')

print(df_base_pivot.head())

# Reordena os níveis para: produto > tipo (meta/vendas) > mês
df_base_pivot.columns = df_base_pivot.columns.reorder_levels([1, 0, 2])


df_ranking = df_base_pivot

for produto in produtos:
    for tipo in tipos:
        df_ranking[(produto, tipo, 'total')] = (
            df_ranking[(produto, tipo, 1)] +
            df_ranking[(produto, tipo, 2)] +
            df_ranking[(produto, tipo, 3)]
        )

for produto in produtos:
    df_ranking[(produto,'resultado','%')] = (
        df_ranking[(produto, 'vendas', 'total')] /
        df_ranking[(produto, 'meta', 'total')]
    )

    df_ranking[(produto, 'pontos', '')] = np.floor(
        df_ranking[(produto, 'resultado', '%')] * 10
    )


# Ordena os níveis para Produto(level 0) > Tipo(level 1) > Mês(level 2)

df_ranking = df_ranking.sort_index(axis=1, level=[0])

print(df_ranking.head())