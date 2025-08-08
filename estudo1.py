import pandas as pd
from pyparsing import col

df = pd.read_excel("base_dados.xlsx")

# Etapa 1: renomeia os produtos em ordem de prioridade para facilidar o pivot na ordenação
df['produto'] = df['produto'].replace({
    'Chocolate': '1.Chocolate',
    'Biscoito': '2.Biscoito',
    'Snack': '3.Snack'
})

df_pivot = df.pivot_table(index='vendedor', columns=['produto', 'mes'], values=['meta', 'vendas'], aggfunc='sum')

# Reordena os níveis para: produto > tipo (meta/vendas) > mês
df_pivot.columns = df_pivot.columns.reorder_levels([1, 0, 2])

# Ordena os níveis para Produto(level 0) > Tipo(level 1) > Mês(level 2)
df_pivot = df_pivot.sort_index(axis=1, level=[0,1,2])


# Achata o MultiIndex para colunas simples
colunas = [f"{produto}_{tipo}_{mes}" for produto, tipo, mes in df_pivot.columns]

colunas = [col.split('.')[1] if '.' in col else col for col in colunas]

df_pivot.columns = colunas

df_ranking = df_pivot

print(df_ranking.head())