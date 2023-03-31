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

# comando para juntar as paginas
st.set_page_config(page_title='Overall', layout='wide')


# =============================================================================
                                ## Funções ##
# =============================================================================
def clean_code(df1):
    """ Esta função tem a responsabilidade de limpar o dataframe.
        Tipos de limpeza:
            1. Trocar os 'Country Code' para o respectivo pais;
            2. Criação do Tipo de Categoria de Comida;
            3. Criação do nome das Cores;
            4. Deletar colunas desnecessarias;
            5. Remoção dos dados nulos; 
            6. Selecionar um unico valor de uma coluna que possui mais de um valor;
            7. Renomear as colunas do DataFrame.
        Imput: Dataframe
        Output: Dataframe Limpo
    """   
    # 1. Preenchimento do nome dos países (passando cada cosigo da cóluna 'Country Code' para o seu respectivo pais)
    COUNTRIES = {
                1: "India",
                14: "Australia",
                30: "Brazil",
                37: "Canada",
                94: "Indonesia",
                148: "New Zeland",
                162: "Philippines",
                166: "Qatar",
                184: "Singapure",
                189: "South Africa",
                191: "Sri Lanka",
                208: "Turkey",
                214: "United Arab Emirates",
                215: "England",
                216: "United States of America",
                }
    df1['Country Code'] = df1['Country Code'].apply(lambda x: COUNTRIES[x])
        
    # 2. Criação do Tipo de Categoria de Comida
    RANGES_FOOD = {
                    1: "cheap",
                    2: "normal",
                    3: "expensive",
                    4: "gourmet"
                    }
    df1['Price range'] = df1['Price range'].apply(lambda x: RANGES_FOOD[x])
    
    # 3. Criação do nome das Cores
    COLORS = {
            "3F7E00": "darkgreen",
            "5BA829": "green",
            "9ACD32": "lightgreen",
            "CDD614": "orange",
            "FFBA00": "red",
            "CBCBC8": "darkred",
            "FF7800": "darkred",
            }
    df1['Rating color'] = df1['Rating color'].apply(lambda x: COLORS[x])
    
    # 4. Deletando a coluna 'Switch to order menu' (pois ela so possui o valor 0, o que não é muito util.)
    df1 = df1.drop('Switch to order menu', axis=1)
    
    # 5. Deletando valores nulos
    df1 = df1.dropna()
    df1 = df1.reset_index()
    
    #  6. Selecionando somente o primeiro tipo de culinaria da coluna 'Cuisines'
    df1["Cuisines"] = df1.loc[:, "Cuisines"].apply(lambda x: x.split(",")[0])

    # 7. Renomear as colunas do DataFrame
    df1.rename(columns={
                    'Restaurant ID': 'Restaurant_ID', 
                    'Restaurant Name': 'Restaurant_name',
                    'Country Code': 'Country',
                    'Locality Verbose': 'Locality_verbose',
                    'Average Cost for two': 'Average_cost_for_two', 
                    'Has Table booking': 'Has_table_booking',
                    'Has Online delivery': 'Has_online_delivery', 
                    'Is delivering now': 'Is_delivering_now', 
                    'Price range': 'Price_range',
                    'Aggregate rating': 'Aggregate_rating', 
                    'Rating color': 'Rating_color', 
                    'Rating text': 'Rating_text'
                    }, inplace=True)    
    
    # 8. Criando uma coluna com todos os valores da coluna 'Average_cost_for_two' em Dolar
    moeda = { 'Botswana Pula(P)': 0.075,
    'Brazilian Real(R$)':     0.19,
    'Emirati Diram(AED)':     0.27, 
    'Indian Rupees(Rs.)':     0.012,
    'Indonesian Rupiah(IDR)': 0.000065, 
    'NewZealand($)':          0.617486, 
    'Pounds(£)':              1.1947,
    'Qatari Rial(QR)':        0.27, 
    'Rand(R)':                0.054, 
    'Sri Lankan Rupee(LKR)':   0.0031,
    'Turkish Lira(TL)':        0.053}

    df1['Average_cost_for_two_Dollar'] = df1.loc[:, 'Average_cost_for_two']
    for i in moeda:
      print(moeda[i])
      df1.loc[df1.loc[:, 'Currency']==i, 'Average_cost_for_two_Dollar'] = df1.loc[df1.loc[:, 'Currency']==i, 'Average_cost_for_two']*moeda[i]
        
    # 9. Removendo um outlier
    df1.drop(385,axis=0,inplace=True)

    return df1

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




# ===========================================================================================================
                                ## Inicio da estrutura lógica do código ##
# ===========================================================================================================


# -----------------------------------------------------
# Importando os dados
# -----------------------------------------------------
df = pd.read_csv('dataset/zomato.csv')


# -----------------------------------------------------
# limpando os dados
# -----------------------------------------------------
df1 = clean_code(df)


# =============================================================================
                        ## Barra lateral no Streamlit ##    
# =============================================================================
#image_path = 'C:/Users/leona/Documents/repos/FTC/projeto_final/logo_Delicious.png'
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



# =============================================================================
                        ## Layout no Streamlit
# =============================================================================
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