import streamlit as st
import plotly_express as px

def grafico_barra_emp(df, titulo, eixo_x, eixo_y, cores):
    
    st.subheader(titulo)

    # Ordena por posição
    df = df.sort_values(by='Posição', ascending=False)
  
    fig = px.bar(
        df,
        x=eixo_x,
        y=eixo_y,
        orientation='h',
        text_auto=True,
        color_discrete_map=cores,
        title="",
        height=800,
        labels={"variable": ""},
    )

    # adiciona total à direita das barras como inteiro
    df['Total'] = df[eixo_x].sum(axis=1)
    for i, row in df.iterrows():
        fig.add_annotation(
            x=row['Total'] + 1,
            y=row[eixo_y],
            text=str(int(row['Total'])),
            showarrow=False,
            xanchor='left',
            yanchor='middle'
        )


    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        barmode='stack',
        font=dict(size=14),
        margin=dict(r=100),
        yaxis=dict(tickfont=dict(size=16, color=st.get_option("theme.textColor"))),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1,
            xanchor="right",
            x=1,
            font=dict(
                size=14,
                color=st.get_option("theme.textColor")
            )    
        )
    )

    # esconde os rótulos do eixo X
    fig.update_xaxes(showticklabels=False)

    st.plotly_chart(fig, use_container_width=True)