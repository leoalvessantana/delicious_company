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
st.set_page_config(page_title='Cities', layout='wide')


# -----------------------------------------------------
# Importando os dados
# -----------------------------------------------------
df = pd.read_csv('dataset/zomato.csv')


# -----------------------------------------------------
# limpando os dados
# -----------------------------------------------------
df1 = aux_function.clean_code(df)


# -----------------------------------------------------
# Barra lateral no Streamlit ##    
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
st.markdown('# Cities')


with st.container():
    # Top 10 cities with restaurants with an average score above 4:
    st.markdown('## Top 10 Cities with Restaurants with an Average Score Above 4')

    df_aux = df1.loc[df1.loc[:, 'Aggregate_rating']>4.0, ['City', 'Restaurant_ID']].groupby('City').nunique().reset_index()
    df_aux = df_aux.sort_values('Restaurant_ID', ascending=False).iloc[0:10,:]

    Country = []
    for i in df_aux.index:
        city = df_aux.loc[i, 'City']
        Country.append(df1.loc[df1.loc[:, 'City']==city, 'Country'].iloc[0])

    df_aux['Country'] = Country

    # gráfico
    fig = px.bar(df_aux, x='City', y='Restaurant_ID', 
                 labels={'Restaurant_ID': 'Number of Restaurants'},
                 hover_data=['Country'],
                 text = df_aux['Country'].apply(lambda x: x if x!='United States of America' else 'USA' ))
    fig.update_traces(marker_color='#94381F')
    st.plotly_chart(fig, use_container_width=True)

    
    
with st.container():
    # Top 10 cities with restaurants with an average score below 2.5?
    st.markdown('## Top 10 Cities with Restaurants with an Average Score Below 2.5')
    df_aux = df1.loc[df1.loc[:, 'Aggregate_rating']<2.5, ['City', 'Restaurant_ID']].groupby('City').nunique().reset_index()
    df_aux = df_aux.sort_values('Restaurant_ID', ascending=False).iloc[0:10,:]

    Country = []
    for i in df_aux.index:
        city = df_aux.loc[i, 'City']
        Country.append(df1.loc[df1.loc[:, 'City']==city, 'Country'].iloc[0])

    df_aux['Country'] = Country

    # gráfico
    fig = px.bar(df_aux, x='City', y='Restaurant_ID', 
                 labels={'Restaurant_ID': 'Number of Restaurants'},
                 hover_data=['Country'],
                 text = df_aux['Country'].apply(lambda x: x if x!='United States of America' else 'USA' ))
    fig.update_traces(marker_color='#94381F')
    st.plotly_chart(fig, use_container_width=True)
    
    
    
with st.container():
    # Top 10 Cities with the Most Distinct Types of Cuisine?
    st.markdown('## Top 10 Cities with the Most Distinct Types of Cuisines')
    df_aux = df1.loc[:, ['City', 'Cuisines']].groupby('City').nunique().reset_index()
    df_aux = df_aux.sort_values('Cuisines', ascending=False).iloc[0:10, :]
    
    Country = []
    for i in df_aux.index:
        city = df_aux.loc[i, 'City']
        Country.append(df1.loc[df1.loc[:, 'City']==city, 'Country'].iloc[0])
        
    df_aux['Country'] = Country

    # gráfico
    fig = px.bar(df_aux, x='City', y='Cuisines', 
                 labels={'Cuisines': 'Number of Cuisines'},
                 hover_data=['Country'],
                 text = df_aux['Country'].apply(lambda x: x if x!='United States of America' else 'USA' ))
    fig.update_traces(marker_color='#94381F')
    st.plotly_chart(fig, use_container_width=True)
    
    
    