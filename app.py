import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

st.set_page_config(layout='wide')
st.header('Dashboard')

# Carregar e preparar dados da primeira guia (ICMS)
df1 = pd.read_excel('./dados/planilha.xlsx', sheet_name='ICMS')
df1 = df1[df1['Competência'] != 'TOTAL:']
df1['Competência'] = pd.to_datetime(df1['Competência'], format='%b/%y', errors='coerce')
df1 = df1.dropna(subset=['Competência'])
df1 = df1[df1['Competência'].dt.month <= 6]
df1_melted = df1.melt(id_vars='Competência', var_name='Loja', value_name='ICMS')

# Gráficos da primeira guia (ICMS)
col1, col2 = st.columns(2)

with col1:
    st.title('ICMS')
    grafico_icms_linhas = alt.Chart(df1_melted).mark_line(point=alt.OverlayMarkDef(size=80)).encode(
        x=alt.X('yearmonth(Competência):T', title='Mês/Ano', axis=alt.Axis(format='%b %Y')),
        y=alt.Y('ICMS:Q', title='Receita', axis=alt.Axis(format='~s')),
        color='Loja:N',
        tooltip=[
            alt.Tooltip('Competência:T', format='%b %Y'),
            alt.Tooltip('Loja:N'),
            alt.Tooltip('ICMS:Q', format=',.2f')
        ]
    ).properties(height=400).configure_axis(
        labelFontSize=12, titleFontSize=14
    ).configure_legend(
        labelFontSize=12, titleFontSize=14
    ).configure_view(stroke='transparent')
    
    st.altair_chart(grafico_icms_linhas, use_container_width=True)

with col2:
    st.title('Totais')
    df1_totais = df1.iloc[:, 1:].sum().reset_index()
    df1_totais.columns = ['Loja', 'Total ICMS']
    grafico_total_icms = px.bar(df1_totais, x='Loja', y='Total ICMS', text_auto=True, title='Total de ICMS arrecadado p/mês')
    grafico_total_icms.update_layout(xaxis_title='Lojas', height=400)
    
    st.plotly_chart(grafico_total_icms, use_container_width=True)

#####################################################################################################################################################

st.markdown("---")

# Carregar e preparar dados da segunda guia (FATURAMENTO)
df2 = pd.read_excel('./dados/planilha.xlsx', sheet_name='Faturamento por loja')

# Preservar a coluna 'Total mês' em uma cópia do DataFrame para uso no gráfico de pizza
df2_copy = df2.copy()

# Remover a coluna 'Total mês' do DataFrame original para gráficos de linha e barras
if 'Total mês' in df2.columns:
    df2 = df2.drop(columns=['Total mês'])

df2 = df2[df2['Competência'] != 'TOTAL:']
df2['Competência'] = pd.to_datetime(df2['Competência'], format='%b/%y', errors='coerce')
df2 = df2.dropna(subset=['Competência'])
df2 = df2[df2['Competência'].dt.month <= 6]
df2_melted = df2.melt(id_vars='Competência', var_name='Loja', value_name='Faturamento')

# Gráficos da segunda guia (FATURAMENTO)
col3, col4 = st.columns(2)

with col3:
    st.title('Faturamento por loja')
    grafico_faturamento_linhas2 = alt.Chart(df2_melted).mark_line(point=alt.OverlayMarkDef(size=80)).encode(
        x=alt.X('yearmonth(Competência):T', title='Mês/Ano', axis=alt.Axis(format='%b %Y')),
        y=alt.Y('Faturamento:Q', title='Receita', axis=alt.Axis(format='~s')),
        color='Loja:N',
        tooltip=[
            alt.Tooltip('Competência:T', format='%b %Y'),
            alt.Tooltip('Loja:N'),
            alt.Tooltip('Faturamento:Q', format=',.2f')
        ]
    ).properties(height=400).configure_axis(
        labelFontSize=12, titleFontSize=14
    ).configure_legend(
        labelFontSize=12, titleFontSize=14
    ).configure_view(stroke='transparent')
    
    st.altair_chart(grafico_faturamento_linhas2, use_container_width=True)

with col4:
    df2_totais = df2.iloc[:, 1:].sum().reset_index()
    df2_totais.columns = ['Loja', 'Faturamento']
    grafico_total_faturamento = px.bar(df2_totais, x='Loja', y='Faturamento', text_auto=True, title='Faturamento total de cada loja p/mês')
    grafico_total_faturamento.update_layout(xaxis_title='Lojas', height=400)
    
    st.plotly_chart(grafico_total_faturamento, use_container_width=True)

# Adicionando gráfico de pizza para a coluna "Total DE FATURAMENTO P/MÊS SOMANDO AS 7 LOJAS"
col5, col6 = st.columns(2)

with col5:
    if 'Total mês' in df2_copy.columns:
        # Converter a coluna 'Competência' em df2_copy para datetime
        df2_copy['Competência'] = pd.to_datetime(df2_copy['Competência'], format='%b/%y', errors='coerce')
        df2_copy = df2_copy.dropna(subset=['Competência'])
        
        # Filtrar os valores até o mês de junho
        df_total_mes = df2_copy[['Competência', 'Total mês']]
        df_total_mes = df_total_mes[df_total_mes['Competência'].dt.month <= 6]
        
        # Somar os valores de 'Total mês' até junho
        df_total_mes_sum = df_total_mes.groupby('Competência')['Total mês'].sum().reset_index()

        # Formatar a competência para mostrar o nome do mês e ano
        df_total_mes_sum['Competência'] = df_total_mes_sum['Competência'].dt.strftime('%B %Y')

        grafico_pizza_total_mes = px.pie(
            df_total_mes_sum,
            values='Total mês',
            names='Competência',
            title='Faturamento total de cada mês (somando as 7 lojas)'
        )

        st.plotly_chart(grafico_pizza_total_mes, use_container_width=True)
        
################################################################################################################################################################

st.markdown("---")

# Carregar e preparar dados da terceira guia (AMPARA)
df3 = pd.read_excel('./dados/planilha.xlsx', sheet_name='AMPARA RS')
df3 = df3[df3['Competência'] != 'TOTAL:']
df3['Competência'] = pd.to_datetime(df3['Competência'], format='%b/%y', errors='coerce')
df3 = df3.dropna(subset=['Competência'])
df3 = df3[df3['Competência'].dt.month <= 6]
df3_melted = df3.melt(id_vars='Competência', var_name='Loja', value_name='Valor')

# Gráficos da terceira guia
col7, col8 = st.columns(2)

with col7:
    st.title('Ampara')

    # Gráfico de linhas com pontos menores
    grafico_valor_linhas3 = alt.Chart(df3_melted).mark_line(point=alt.OverlayMarkDef(size=50)).encode(
        x=alt.X('yearmonth(Competência):T', title='Mês/Ano', axis=alt.Axis(format='%b %Y')),
        y=alt.Y('Valor:Q', title='Receita', axis=alt.Axis(format='~s')),
        color='Loja:N',
        tooltip=[
            alt.Tooltip('Competência:T', format='%b %Y'),
            alt.Tooltip('Loja:N'),
            alt.Tooltip('Valor:Q', format=',.2f')
        ]
    ).properties(height=400)

    # # Adicionar rótulos sobre as marcações com o valor exato
    # rotulos_valor = alt.Chart(df3_melted).mark_text(align='left', dx=5, dy=-5, size=15).encode(
    #     x=alt.X('yearmonth(Competência):T'),
    #     y=alt.Y('Valor:Q'),
    #     text=alt.Text('Valor:Q', format=',.2f'),
    #     color='Loja:N'
    # )

    # Combinar os dois gráficos
    grafico_final = grafico_valor_linhas3 #+ rotulos_valor

    # Aplicar configurações no gráfico combinado
    grafico_final = grafico_final.configure_axis(
        labelFontSize=12, titleFontSize=14
    ).configure_legend(
        labelFontSize=12, titleFontSize=14
    ).configure_view(stroke='transparent')

    # Exibir o gráfico
    st.altair_chart(grafico_final, use_container_width=True)

with col8:
    df3_totais = df3.iloc[:, 1:].sum().reset_index()
    df3_totais.columns = ['Loja', 'Receita']
    grafico_total_valor3 = px.bar(df3_totais, x='Loja', y='Receita', text_auto=True, title='Total de AMPARA arrecadado p/mês')
    grafico_total_valor3.update_layout(xaxis_title='Lojas', height=400)
    
    st.plotly_chart(grafico_total_valor3, use_container_width=True)

###################################################################################################################################################################
    
st.markdown("---")

# Carregar e preparar dados da guia (PIS e COFINS)
df4 = pd.read_excel('./dados/planilha.xlsx', sheet_name='PISCOFINS')
df4 = df4[df4['Competência'] != 'TOTAL:']
df4['Competência'] = pd.to_datetime(df4['Competência'], format='%b/%y', errors='coerce')
df4 = df4.dropna(subset=['Competência'])
df4 = df4[df4['Competência'].dt.month <= 6]
df4.columns = df4.columns.str.strip()

# Derreter os dados para criar as linhas de PIS e COFINS no mesmo gráfico
df4_melted = df4.melt(id_vars='Competência', value_vars=['PIS', 'COFINS'], var_name='Imposto', value_name='Valor')

# Gráfico de linha para PIS e COFINS
st.title('PIS e COFINS')
grafico_pis_cofins_linhas = alt.Chart(df4_melted).mark_line(point=alt.OverlayMarkDef(size=60)).encode(
    x=alt.X('yearmonth(Competência):T', title='Mês/Ano', axis=alt.Axis(format='%b %Y')),
    y=alt.Y('Valor:Q', title='Valor', axis=alt.Axis(format='~s')),
    color=alt.Color('Imposto:N', title='Imposto'),
    tooltip=[
        alt.Tooltip('Competência:T', format='%b %Y'),
        alt.Tooltip('Imposto:N'),
        alt.Tooltip('Valor:Q', format=',.2f')
    ]
).properties(height=400).configure_axis(
    labelFontSize=12, titleFontSize=14
).configure_legend(
    labelFontSize=12, titleFontSize=14
).configure_view(stroke='transparent')

st.altair_chart(grafico_pis_cofins_linhas, use_container_width=True)

# Calcular o total de PIS e COFINS
total_pis = df4['PIS'].sum()
total_cofins = df4['COFINS'].sum()

# Criar um DataFrame para o gráfico de pizza
df_total = pd.DataFrame({
    'Imposto': ['PIS', 'COFINS'],
    'Total': [total_pis, total_cofins]
})

# Gráfico de pizza
st.title('Distribuição Total de PIS e COFINS')
grafico_pizza = px.pie(
    df_total,
    values='Total',
    names='Imposto',
    title='Total de PIS e COFINS (Janeiro a Junho)'
)

st.plotly_chart(grafico_pizza, use_container_width=True)