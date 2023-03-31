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
st.set_page_config(page_title='Countries', layout='wide')


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
