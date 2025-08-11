import streamlit as st
import plotly_express as px

def grafico_barra_emp(df, titulo):
    st.subheader(titulo)

    pontos_cols = [(produto, "Pontos") for produto in ['Chocolate', 'Biscoito', 'Snack']]
    colunas = [("Vendedor", ""), ("Posição", "")] + pontos_cols
    df_grafico = df[colunas].copy()
    df_grafico.columns = ['Vendedor', 'Posição', 'Chocolate', 'Biscoito', 'Snack']

    # Ordena por posição
    df_grafico = df_grafico.sort_values(by='Posição', ascending=False)

    # Soma total dos pontos
    df_grafico['Total'] = df_grafico[['Chocolate', 'Biscoito', 'Snack']].sum(axis=1)

    # Cria coluna para o eixo Y com "Posição - Vendedor"
    df_grafico['Posição_Vendedor'] = df_grafico['Posição'].astype(str) + " - " + df_grafico['Vendedor']

    fig = px.bar(
        df_grafico,
        y='Posição_Vendedor',
        x=['Chocolate', 'Biscoito', 'Snack'],
        orientation='h',
        text_auto=True,
        color_discrete_map={
            'Chocolate': '#502172',
            'Biscoito': '#0071b8',
            'Snack': '#00b2c4'
        },
        height=800,
        labels={"variable": ""}
    )

    # Adiciona total à direita das barras como inteiro
    for i, row in df_grafico.iterrows():
        fig.add_annotation(
            x=row['Total'] + 1,
            y=row['Posição_Vendedor'],
            text=str(int(row['Total'])),
            showarrow=False,
            font=dict(size=16, color='black'),
            xanchor='left',
            yanchor='middle'
        )

    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        barmode='stack',
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=14),
        margin=dict(r=100),
        yaxis=dict(tickfont=dict(size=16))
    )

    # Esconde os rótulos do eixo X
    fig.update_xaxes(showticklabels=False)

    st.plotly_chart(fig, use_container_width=True)