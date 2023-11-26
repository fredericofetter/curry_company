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

st.sidebar.markdown('### Filtros')

countries_selected = st.sidebar.multiselect(
    'Escolha os países que deseja visualizar as Informações', 
    get_countries(df1), default=['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia']
)


n_top_rest = st.sidebar.slider(
    '### Quantas cidades com mais restaurantes quer visualizar', 
    value=10, 
    min_value=1, 
    max_value=20,
)


agg_upper_cutoff = st.sidebar.slider(
    '### Qual a maior avaliação de restaurantes que deseja visualizar', 
    value=4., 
    min_value=1., 
    max_value=5.,
    step=0.05
)

    

agg_lower_cutoff = st.sidebar.slider(
    '### Qual a menor avaliação de restaurantes que deseja visualizar', 
    value=3., 
    min_value=1., 
    max_value=5.,
    step=0.05
)


n_top_cuisines = st.sidebar.slider(
    '### Quantas cidades com mais culinárias quer visualizar', 
    value=10, 
    min_value=1, 
    max_value=20,
)


##########################################################################################
# CAMPO PRINCIPAL
##########################################################################################


st.markdown('# 	:cityscape: Visão Cidades')

linhas_selecionadas = df1['country_code'].apply( country_name ).isin( countries_selected )
df1 = df1[linhas_selecionadas]


#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------


with st.container():
    plot_cities_bars(df1, y_ax='restaurant_id', n_top=n_top_rest, agg_upper_cutoff=10, agg_lower_cutoff=-1)
    
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
    
with st.container():
    col1, col2 = st.columns( 2 )

#-------------------------------------------------------------------------------------------
   
    with col1.container():
        plot_cities_bars(df1, y_ax='aggregate_rating', n_top=7, agg_upper_cutoff=10, agg_lower_cutoff=agg_lower_cutoff)
        
#-------------------------------------------------------------------------------------------
        
    with col2.container():
        plot_cities_bars(df1, y_ax='aggregate_rating', n_top=7, agg_upper_cutoff=agg_upper_cutoff, agg_lower_cutoff=-1)

#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------

with st.container():
    plot_cities_bars(df1, y_ax='cuisines', n_top=n_top_cuisines, agg_upper_cutoff=10, agg_lower_cutoff=-1)
    
    
