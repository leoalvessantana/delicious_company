# Bibliotecas
import pandas as pd
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static
from aux_function import aux_function 


# -----------------------------------------------------
# comando para juntar as paginas
# -----------------------------------------------------
st.set_page_config(page_title='Cuisines', layout='wide')


# -----------------------------------------------------
# Importando os dados
# -----------------------------------------------------
# caminho = 'C:/Users/leona/Documents/repos/FTC/projeto_final/dataset/zomato.csv'
df = pd.read_csv('dataset/zomato.csv')


# -----------------------------------------------------
# limpando os dados
# -----------------------------------------------------
df1 = aux_function.clean_code(df)


# -----------------------------------------------------
# Barra lateral no Streamlit     
# -----------------------------------------------------
image = Image.open('logo_Delicious.png')
st.sidebar.image(image, width=150)

country_slider = st.sidebar.multiselect(
    'Select the Country:',
    ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'],
    default=['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'])
st.sidebar.markdown(""" --- """)

st.sidebar.markdown('###### Powered by Leonardo Santana')
st.sidebar.markdown('###### Data Scientist @ Comunidade DS')


# # Filtros de transito
linhas_selecionadas = df1['Country'].isin(country_slider)
df1 = df1.loc[linhas_selecionadas, :]



# -----------------------------------------------------
# Layout no Streamlit
# -----------------------------------------------------
st.markdown('# Cuisines')

with st.container():
    col1, col2 = st.columns(2, gap='large')
    with col1:
        # Top 10 best types of cuisines
        st.markdown('## Top 10 Best Types of Cuisines')
        df_aux = df1.loc[:, ['Cuisines', 'Aggregate_rating']].groupby('Cuisines').mean().reset_index()
        df_aux = df_aux.sort_values('Aggregate_rating', ascending=False).iloc[0:10, :]
        fig = px.bar(df_aux, x='Cuisines', y='Aggregate_rating', labels={'Aggregate_rating': 'Aggregate rating'}, text_auto='.2s')
        fig.update_traces(marker_color='#94381F')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        # Top 10 worst types of cuisines
        st.markdown('## Top 10 Worst Types of Cuisines')
        df_aux = df1.loc[:, ['Cuisines', 'Aggregate_rating']].groupby('Cuisines').mean().reset_index()
        df_aux = df_aux.sort_values('Aggregate_rating', ascending=True).iloc[0:10, :]
        fig = px.bar(df_aux, x='Cuisines', y='Aggregate_rating', labels={'Aggregate_rating': 'Aggregate rating'}, text_auto='.2s')
        fig.update_traces(marker_color='#94381F')
        st.plotly_chart(fig, use_container_width=True)       

        
with st.container():    
    # The 10 best types of cuisine that have the highest average value of a dish for two people
    st.markdown('## The 10 Best Types of Cuisine that have the Highest Average Value of a Dish For Two People')
    df_aux = df1.loc[:, ['Cuisines', 'Average_cost_for_two']].groupby('Cuisines').mean().reset_index()
    df_aux = df_aux.sort_values('Average_cost_for_two', ascending=False).iloc[0:10, :]
    fig = px.bar(df_aux, x='Cuisines', y='Average_cost_for_two', labels={'Average_cost_for_two': 'Average cost for two'}, text_auto='.2s')
    fig.update_traces(marker_color='#94381F')
    st.plotly_chart(fig, use_container_width=True)
    
with st.container():
    # All restaurants with the highest average score (4.9/5.0)
    st.markdown('## All Restaurants with the Highest Average Score (4.9/5.0)')
    df_aux = df1.sort_values('Aggregate_rating', ascending=False).head(255)
    df_aux = df_aux.loc[:, ['Cuisines', 'Restaurant_name', 'Country', 'City', 'Average_cost_for_two', 'Currency', 'Aggregate_rating', 'Votes']]
    df_aux = df_aux.sort_values(['Cuisines', 'Country', 'City'], ascending=True)
    st.dataframe(df_aux)