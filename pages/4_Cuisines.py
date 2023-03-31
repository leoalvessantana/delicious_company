# Bibliotecas
import pandas as pd
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static

# comando para juntar as paginas
st.set_page_config(page_title='Cuisines', layout='wide')


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



# ===========================================================================================================
                                ## Inicio da estrutura lógica do código ##
# ===========================================================================================================


# -----------------------------------------------------
# Importando os dados
# -----------------------------------------------------
# caminho = 'C:/Users/leona/Documents/repos/FTC/projeto_final/dataset/zomato.csv'
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