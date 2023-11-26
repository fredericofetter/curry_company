# Libraries
import pandas as pd
import streamlit as st

import plotly.express as px
import inflection

from PIL import Image

import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

from utils import *

# https://github.com/blackary/st_pages/



##########################################################################################
# Loading Data
##########################################################################################


# Import dataset
df = pd.read_csv( 'dataset/zomato.csv' )

df1 = df.copy() #copied to preserve original dataframe



##########################################################################################
# LIMPEZA
##########################################################################################

df1 = clean_data(df1)

##########################################################################################
# BARRA LATERAL
##########################################################################################

with st.container():

    image_path = 'images/logo_app_ftc.png'
    image = Image.open( image_path )

    st.sidebar.image( image, width=285 )

    st.markdown("""
    <style>
    .big-font {
        font-size:55px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.markdown('<p class="big-font">Fome Zero</p>', unsafe_allow_html=True)

#    st.sidebar.text( 'Fome Zero' )

#----------------------------------

st.sidebar.markdown( """---""" )

with st.container():

    st.sidebar.markdown('### Filtros')

    countries_selected = st.sidebar.multiselect(
        'Escolha os países que deseja visualizar as Informações', 
        get_countries(df1), default=['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia']
    )




##########################################################################################
#                       CAMPO PRINCIPAL
##########################################################################################


st.markdown('# :earth_americas: Visão Países')


linhas_selecionadas = df1['country_code'].apply(country_name).isin( countries_selected )
df1 = df1[linhas_selecionadas]



#---------------------------------------------------------------------
#---------------------------------------------------------------------

with st.container():
    
    plot_countries_bars(df1=df1, y_ax='restaurant_id')
    
#---------------------------------------------------------------------
#---------------------------------------------------------------------
    
    
    
with st.container():

    plot_countries_bars(df1=df1, y_ax='city')
    
    
#---------------------------------------------------------------------
#---------------------------------------------------------------------

    
    
with st.container():
    col1, col2 = st.columns( 2 )
    
#---------------------------------------------------------------------
 
    col1.markdown( '### Média de avaliações por país.' )
    
    with col1.container():
    
        plot_countries_bars(df1=df1, y_ax='votes')
    
#---------------------------------------------------------------------
    
    col2.markdown( '### Média do custo médio para duas pessoas')
    
    with col2.container():
            
        plot_countries_bars(df1=df1, y_ax='average_cost_for_two')