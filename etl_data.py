import pandas as pd
import numpy as np

def gerar_coluna_kpi(df, produto, mes):
    df_coluna = df[(df['produto'] == produto) & (df['mes'] == mes)]
    df_coluna = df_coluna.drop(['produto','mes'], axis=1)
    df_coluna = df_coluna.rename(columns = {'meta' : f"{produto}_M{mes}",
                                'vendas' : f"{produto}_V{mes}"})
    return df_coluna


def calcular_total_kpi(df, produto):    
    df[f"{produto}_Meta Total"] = df[f"{produto}_M1"] + df[f"{produto}_M2"] +df[f"{produto}_M3"]
    df[f"{produto}_Vendas Total"] = df[f"{produto}_V1"] + df[f"{produto}_V2"] +df[f"{produto}_V3"]
    return df


def calcular_resultado_kpi(df, produto):    
    df[f"{produto}_Resultado"] = df[f"{produto}_Vendas Total"] / df[f"{produto}_Meta Total"]
    return df


def calcular_pontos_kpi(df, produto):    
    df[f"{produto}_Pontos"] = np.floor(df[f"{produto}_Resultado"] * 10)
    return df


def calcular_pontuacao_geral(df, produtos):
    df["Pontuação"] = df[[f"{p}_Pontos" for p in produtos]].sum(axis=1)
    return df


def reordenar_colunas(df, produtos, tipos, meses):
    ordem_colunas = ['vendedor']
    for produto in produtos:
        for tipo in tipos:
            for mes in meses:               
                ordem_colunas.append(f"{produto}_{tipo[0]}{mes}")
            ordem_colunas.append(f"{produto}_{tipo} Total")
        ordem_colunas.append(f"{produto}_Resultado")
        ordem_colunas.append(f"{produto}_Pontos")
    ordem_colunas.append("Pontuação")
    df = df[ordem_colunas]

    return df


def ordenar_posicao(df, produtos):
    df.sort_values(by=['Pontuação'] + [f"{produto}_Pontos" for produto in produtos], ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.insert(0, 'Posição', df.index + 1)

    return df


def formatar_numeros(df):

    for col in df.columns:
        if col[-1].isdigit() or 'Total' in col:
            df[col] = df[col].map(lambda x: f"{x:,.0f}".replace(",", "."))
        elif 'Resultado' in col:
            df[col] = df[col].map('{:.1%}'.format)
    
    return df


def multiindex_colunas(df):
    lista_tuplas_colunas = []
    colunas = df.columns
    for coluna in colunas:
        if "_" in coluna:
            lista_tuplas_colunas.append(tuple(coluna.split('_')))
        else:
            lista_tuplas_colunas.append((coluna.capitalize(), ""))

    df.columns = pd.MultiIndex.from_tuples(lista_tuplas_colunas)
    
    return df
                 

def etl_data(produtos, tipos, meses):
    # as listas abaixo devem ser colocadas na ordem que as colunas devem aparecer na tabela
    

    df_base = pd.read_excel(".\\data\\base_dados.xlsx")

    # criar o dataframe do ranking através do vendedores únicos
    df_ranking = df_base['vendedor'].drop_duplicates().to_frame().reset_index(drop=True)


    # criar as colunas de meta e vendas de cada produto de cada mes
    for produto in produtos:
        for mes in meses:
            df_mes_produto = gerar_coluna_kpi(df_base, produto,  mes)
            df_ranking = df_ranking.merge(df_mes_produto, on='vendedor')

            # criar a coluna de meta_total, venda_total, resultdo e pontos
            if mes == 3:
                df_ranking = calcular_total_kpi(df_ranking, produto)
                df_ranking = calcular_resultado_kpi(df_ranking, produto)
                df_ranking = calcular_pontos_kpi(df_ranking, produto)

    # criar coluna da pontuação geral
    df_ranking = calcular_pontuacao_geral(df_ranking, produtos)

    # reordenar colunas
    df_ranking = reordenar_colunas(df_ranking, produtos, tipos, meses)

    # ordenar por pontos e critérios e adicionar coluna de posição.
    df_ranking = ordenar_posicao(df_ranking, produtos)

    #formatar os números
    df_ranking = formatar_numeros(df_ranking)

    # transformar as colunas em multiindex
    df_ranking = multiindex_colunas(df_ranking)

    return df_ranking
    # print(df_ranking.head())

