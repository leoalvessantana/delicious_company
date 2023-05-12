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
st.set_page_config(page_title='Countries', layout='wide')


# -----------------------------------------------------
# Importando os dados
# -----------------------------------------------------
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
st.markdown('# Contries')

with st.container(): 
    # Number of Cities Registered
    st.markdown('## Number of Cities Registered')
    df_aux = df1.loc[:, ['Country', 'City']].groupby(['Country']).nunique().reset_index()
    df_aux = df_aux.sort_values('City', ascending=True).iloc[:, :]
    df_aux['city_porc'] = (df_aux.loc[:, 'City']/df_aux.loc[:, 'City'].sum())*100
    fig = px.bar(df_aux, y='Country', x='City', orientation='h',
                 labels={'City': 'Cities'},
                 text=df_aux['city_porc'].apply(lambda x: '{0:.1f}%'.format(x)))
    fig.update_traces(marker_color='#94381F')
    st.plotly_chart(fig, use_container_width=True)


with st.container():
    # Number of Restaurants Registered
    st.markdown('## Number of Restaurants Registered')
    df_aux = df1.loc[:, ['Country', 'Restaurant_ID']].groupby('Country').nunique().reset_index()
    df_aux = df_aux.sort_values('Restaurant_ID', ascending=True)
    df_aux['Restaurant_porc'] = (df_aux.loc[:, 'Restaurant_ID']/df_aux.loc[:, 'Restaurant_ID'].sum())*100
    fig = px.bar(df_aux, y='Country', x='Restaurant_ID', orientation='h', 
                 labels={'Restaurant_ID': 'Restaurants'}, 
                text=df_aux['Restaurant_porc'].apply(lambda x: '{0:.1f}%'.format(x)))
    fig.update_traces(marker_color='#94381F')
    st.plotly_chart(fig, use_container_width=True)

    
with st.container():
    # Average Number of evaluations
    st.markdown('## Average Number of Evaluations')
    df_aux = df1.loc[:, ['Country', 'Votes']].groupby('Country').mean().reset_index()
    df_aux = df_aux.sort_values(by=['Votes'], ascending=False)
    fig = px.bar(df_aux, x='Country', y='Votes', labels={'Votes': 'Evaluation'}, text_auto='.2s')
    fig.update_traces(marker_color='#94381F')
    st.plotly_chart(fig, use_container_width=True)

with st.container():
    # Recorded average score
    st.markdown('## Recorded Average Score')
    df_aux = df1.loc[:, ['Country', 'Aggregate_rating']].groupby('Country').mean().reset_index()
    df_aux = df_aux.sort_values(by=['Aggregate_rating'], ascending=False)
    fig = px.bar(df_aux, x='Country', y='Aggregate_rating', labels={'Aggregate_rating': 'Average score'}, text_auto='.2s')
    fig.update_traces(marker_color='#94381F')
    st.plotly_chart(fig, use_container_width=True)

with st.container():
    # Average Price of a Meal for Two (U.S. Dollar)
    st.markdown('## Average Price of a Meal for Two (U.S. Dollar)')
    df_aux = df1.loc[:, ['Country', 'Average_cost_for_two_Dollar']].groupby('Country').mean().reset_index()
    df_aux = df_aux.sort_values(by=['Average_cost_for_two_Dollar'], ascending=False)
    fig = px.bar(df_aux, x='Country', y='Average_cost_for_two_Dollar', labels={'Average_cost_for_two_Dollar': 'Average cost for two'}, text_auto='.2s')
    fig.update_traces(marker_color='#94381F')
    st.plotly_chart(fig, use_container_width=True)
