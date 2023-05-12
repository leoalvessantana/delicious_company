# Bibliotecas
import numpy as np
import pandas as pd
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from aux_function import aux_function 


# -----------------------------------------------------
# comando para juntar as paginas
# -----------------------------------------------------
st.set_page_config(page_title='Overall', layout='wide')


# -----------------------------------------------------
# Function for map
# -----------------------------------------------------
def restaurant_maps(df1):
    """ Mapa com a localização dos restaurantes.
        Imput: Dataframe
        Output: Mapa
        """

    df1_plot = df1.copy()

    map = folium.Map( zoom_start=11 )

    mc = MarkerCluster().add_to( map )


    for index, location_info in df1_plot.iterrows():
        # Cores nos marcadores
        icon=folium.Icon(color=df1_plot.loc[index, 'Rating_color'], icon='glyphicon-cutlery', prefix='glyphicon')

        # Informação sobre cada restaurante
        html = ('<strong>' + df1_plot.loc[index, 'Restaurant_name'] + '</strong>' + '<br>' + 
              'Cuisine: ' + df1_plot.loc[index, 'Cuisines'] + '<br>' +
              'Price for two: ' + str(df1_plot.loc[index, 'Average_cost_for_two']) + ' ' + df1_plot.loc[index, 'Currency'] 
              )
        iframe = folium.IFrame(html, width=270, height=120)
        popup = folium.Popup(iframe, max_width=300)


        folium.Marker( location = [np.mean(df1_plot.loc[index, 'Latitude']), np.mean(df1_plot.loc[index, 'Longitude'])], 
                    icon=icon, 
                    popup= popup).add_to( mc ) 

    folium_static(map, width=1024, height=600)


    folium.LayerControl().add_to(mc)

    return None
    
    
    
    
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
st.markdown('# Delicious Company')

st.markdown('The best place to find your newest favorite restaurant!')
with st.container(): 
    st.markdown(" ## Some Important Numbers")        

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        # Quantos países únicos estão registrados?
        registred_country = len(df1.loc[:, 'Country'].unique()) 
        col1.metric('Registred Country', registred_country)
    with col2:
        # Quantas cidades únicas estão registradas?
        registred_city = len(df1.loc[:, 'City'].unique())
        col2.metric('Registred City', registred_city)
    with col3:
        # Quantos restaurantes únicos estão registrados?
        registred_restaurant = len(df1.loc[:, 'Restaurant_ID'].unique())
        col3.metric('Registred Restaurant', registred_restaurant)           
    with col4:
        # Qual o total de tipos de culinária registrados?
        registred_cuisines = len(df1.loc[:, 'Cuisines'].unique())
        col4.metric('Registred Cuisines', registred_cuisines) 
    with col5:
        # Qual o total de avaliações feitas?
        registred_votes = df1.loc[:, 'Votes'].sum() 
        col5.metric('Registred Votes', registred_votes) 

            
with st.container():
    st.markdown('## The Location of each Restaurant')
    restaurant_maps(df1)