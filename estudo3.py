import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(page_title="Ranking de Vendedores", layout="wide")
st.title("🏆 Ranking de Vendedores por Produto")

# --- Parâmetros ---
produtos = ['chocolate', 'biscoito', 'snack']
tipos = ['meta', 'vendas']

# --- Carregar base de dados ---
df = pd.read_excel("base_dados.xlsx")

# --- Pivot ---
df_pivot = df.pivot_table(index='vendedor', columns=['produto', 'mes'], values=['meta', 'vendas'], aggfunc='sum')
df_pivot.columns = df_pivot.columns.reorder_levels([1, 0, 2])
df_pivot = df_pivot.sort_index(axis=1, level=[0, 1, 2])
df_pivot.columns = [f"{produto}_{tipo}_{mes}" for produto, tipo, mes in df_pivot.columns]
df_pivot = df_pivot.reset_index(drop=False)
df_pivot.columns = [col.lower() for col in df_pivot.columns]

df_ranking = df_pivot.copy()

# --- Adicionar colunas de totais ---
for produto in produtos:
    for tipo in tipos:
        df_ranking[f"{produto}_{tipo}_total"] = (
            df_ranking[f"{produto}_{tipo}_1"] +
            df_ranking[f"{produto}_{tipo}_2"] +
            df_ranking[f"{produto}_{tipo}_3"]
        )

# --- Adicionar colunas de resultados e pontos ---
for produto in produtos:
    df_ranking[f"{produto}_resultado"] = (
        df_ranking[f"{produto}_vendas_total"] /
        df_ranking[f"{produto}_meta_total"]
    )
    df_ranking[f"{produto}_pontos"] = np.floor(df_ranking[f"{produto}_resultado"] * 10)


# Adicionar coluna de pontuação total ---
df_ranking["pontuacao"] = df_ranking[[f"{p}_pontos" for p in produtos]].sum(axis=1)



novas_colunas = []
for col in df_ranking.columns:
    if col == 'vendedor' or col == 'pontuacao':
        novas_colunas.append((col, ''))  # manter como coluna fora do MultiIndex
    else:
        partes = col.split('_')
        if len(partes) == 3:
            produto, tipo, mes = partes
            if tipo == 'meta':
                nome = f"m{mes}" if mes in ['1', '2', '3'] else 'meta total'
            elif tipo == 'vendas':
                nome = f"v{mes}" if mes in ['1', '2', '3'] else 'vendas total'
            else:
                nome = mes
            novas_colunas.append((produto, nome))
        elif len(partes) == 2:
            produto, tipo = partes
            nome = tipo  # resultado ou pontos
            novas_colunas.append((produto, nome))

# Aplicar novo MultiIndex às colunas
df_ranking.columns = pd.MultiIndex.from_tuples(novas_colunas)

# Separar coluna 'vendedor' e 'pontuacao'
colunas = df_ranking.columns
col_vendedor = [col for col in colunas if col[0] == 'vendedor']
col_pontuacao = [col for col in colunas if col[0] == 'pontuacao']
col_produtos = [col for col in colunas if col[0] in produtos]

# Reorganizar
df_ranking = df_ranking[col_vendedor + col_produtos + col_pontuacao]

# --- Formatar valores (visualmente, mantendo tipos para cálculo se necessário) ---
df_formatado = df_ranking.copy()

for col in df_formatado.columns:
    categoria, subcoluna = col
    if subcoluna in ['m1', 'm2', 'm3', 'meta total', 'v1', 'v2', 'v3', 'vendas total']:
        df_formatado[col] = df_formatado[col].apply(lambda x: f"{x:,.0f}".replace(",", "X").replace(".", ",").replace("X", "."))
    elif subcoluna == 'resultado':
        df_formatado[col] = (df_formatado[col].astype(float) * 100).round(0).astype(int).astype(str) + '%'
    elif subcoluna == 'pontos' or categoria == 'pontuacao':
        df_formatado[col] = df_formatado[col].astype(int).astype(str)

# --- Exibir no Streamlit ---
st.dataframe(df_formatado, use_container_width=True)

# --- Legenda ---
st.markdown("""
### 🛈 Legenda
- **m1, m2, m3**: Metas mensais (meses 1, 2 e 3)  
- **v1, v2, v3**: Vendas mensais (meses 1, 2 e 3)  
- **Meta Total / Vendas Total**: Soma das metas e vendas dos 3 meses  
- **Resultado**: Vendas ÷ Meta  
- **Pontos**: Resultado × 10 (arredondado para baixo)  
- **Pontuação**: Soma dos pontos dos 3 produtos  
""")
