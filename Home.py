import streamlit as st
from PIL import Image


# comando para juntar as paginas
st.set_page_config(layout='wide', page_title="Home", page_icon="🎲")


# sidebar
image = Image.open('logo_Delicious.png')
st.sidebar.image(image, width=150)

st.sidebar.markdown('#### Delicious company informs the best restaurant for you around the world.')
st.sidebar.markdown(""" --- """)

st.sidebar.markdown('###### Powered by Leonardo Santana')
st.sidebar.markdown('###### Data Scientist @ Comunidade DS')




    


st.write("# Delicious Company Dashdoard")

st.markdown(
    """
    #### What you are going to find on this dashboard:
    - Overall:
        - Some Important Numbers.
        - The Location of each Restaurant.

    - Countries:
        - Number of Cities Registered.
        - Number of Restaurants Registered.
        - Average Number of Evaluations.
        - Recorded Average Score.
        - Average Price of a Meal for Two.

    - Cities:
        - Top 10 Cities with Restaurants with an Average Score Above 4.
        - Top 10 Cities with Restaurants with an Average Score Below 2.5.
        - Top 10 Cities with the Most Different Types of Cuisines.  

    - Cuisines:
        - Top 10 Best Types of Cuisines.
        - Top 10 Worst Types of Cuisines.
        - The 10 Best Types of Cuisine that have the Highest Average Value of a Dish For Two People.
        - All Restaurants with the Highest Average Score (4.9/5.0).


    #### Ask for help
    - For questions, suggestions or any other subject related to this dashboard, feel free to contact me on [LinkedIn](https://www.linkedin.com/in/leonardo-alves-santana/).
    
    """
    )