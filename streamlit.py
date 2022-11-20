import streamlit as st
import plotly.express as px
import pandas as pd

df_livros = pd.read_csv('olist data\olist_livros.csv')

df_livros = df_livros.drop(columns=['Unnamed: 0'])

df = pd.read_csv('olist data\linha_temporal.csv')

df_livros['order_approved_at'] = pd.to_datetime(df_livros['order_approved_at'], format='%Y-%m-%d %H:%M:%S')

### Gráficos mês a mês

st.write(' # Gráfico mês a mês')
st.write('Visualizando o número de pedidos ou a renda a cada mês')

option = 'Número de pedidos'

option = st.selectbox('Paulo',('Número de pedidos', 'Renda'), label_visibility='collapsed')

if option == 'Número de pedidos':
    graftempoqte = px.line(df, x='order_approved_at', y='order_item_id', labels={
    'order_item_id': 'Número de pedidos',
    'order_approved_at':'Mês'
    })
    st.plotly_chart(graftempoqte)

if option == 'Renda':
    graftemporenda = px.line(df, x='order_approved_at', y='price', labels={
        'price': 'Renda (em reais)' ,
        'order_approved_at': 'Mês'
    })
    st.plotly_chart(graftemporenda)


### Histograma Recorrência

st.write('# Recorrência')

df1 = df_livros.groupby('customer_unique_id').count().sort_values('order_id', ascending=False)

histrec = px.histogram(df1, x="order_id", labels={
    'order_id':'Quantidade de pedidos por cliente'
    })
histrec.update_layout(bargap=0.5)

st.plotly_chart(histrec)

st.write('# Vendas por estado, ano e trimestre')

estados = list(df_livros['customer_state'].sort_values().unique())

estados = st.multiselect(
    'Selecione os estados',
    estados,
    default=estados
    )

anos = list(df_livros['year'].sort_values().unique())

anos = st.multiselect(
    'Selecione os anos',
    anos,
    default=anos
)

trim = list(df_livros['quarter'].sort_values().unique())

trim = st.multiselect(
    'Selecione os trimestres',
    trim,
    default=trim
)

opcao = st.selectbox('Paulo',('Número de pedidos', 'Renda'), label_visibility='collapsed', key='marceli')

if opcao == 'Número de pedidos':
    a = 'order_item_id'
else:
    a = 'price'

df_estados = df_livros[(df_livros['customer_state'].isin(estados)) & (df_livros['year'].isin(anos)) & (df_livros['quarter'].isin(trim))].groupby('customer_state').sum().reset_index()


grafestados = px.bar(df_estados, x='customer_state', y=a, labels={
        'customer_state': 'Estado' ,
        'order_item_id': 'Número de pedidos',
        'price': 'Renda'
    })
st.plotly_chart(grafestados)