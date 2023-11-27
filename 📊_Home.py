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
# BASIC SETUP
##########################################################################################


st.set_page_config(
    layout="wide", 
#    layout="centered", 
    initial_sidebar_state="expanded", 
    page_icon = ':bar_chart:'
)


pd.set_option("display.max_columns", None) #mostra mais colunas do dataframe
pd.get_option("display.max_columns")

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

#----------------------------------

## Botão de download dos dados

csv = convert_df(df1)

st.sidebar.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='data.csv',
    mime='text/csv',
)



##########################################################################################
# CAMPO PRINCIPAL
##########################################################################################


cont_header = st.container()

cont_header.header('Fome Zero!', divider='rainbow')

cont_header.markdown('## O Melhor lugar para encontrar seu mais novo restaurante favorito!')

cont_header.markdown('### Temos as seguintes marcas dentro da nossa plataforma:')


cont_metric = st.container()

col1, col2, col3, col4, col5 = cont_metric.columns( 5 )

col1.metric('Restaurantes Cadastrados', get_no_rest_cadastrados(df1))

col2.metric('Países Cadastrados', get_no_paises_cadastrados(df1))

col3.metric('Cidades Cadastrados', get_no_cidades_cadastradas(df1))

col4.metric('Avaliações Feitas na Plataforma', get_no_votes(df1))

col5.metric('Tipos de Culinárias Oferecidas', get_no_cuisines(df1))

#----------------------------------------------------------------------------



linhas_selecionadas = df1['country_code'].apply(country_name).isin( countries_selected )
df1 = df1[linhas_selecionadas]

#----------------------------------------------------------------------------

#with st.container():
#    st.dataframe(df1)

#----------------------------------------------------------------------------
    
with st.container():
    plot_map(df1)
