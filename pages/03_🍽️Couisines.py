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

no_rest_viz = st.sidebar.slider(
    '### Selecione a quantidade de Restaurantes que deseja visualizar', 
    value=10, 
    min_value=0, 
    max_value=20,
    #format='DD-MM-YYYY'
)


cuisines_selected = st.sidebar.multiselect(
    'Escolha as culinárias que deseja incluir na tabela dos melhores restaurantes', 
    get_cuisines(df1), default=['Home-made', 'BBQ', 'Japanese', 'Brazilian', 'Arabian', 'American', 'Italian']
)

##########################################################################################
#                       CAMPO PRINCIPAL
##########################################################################################


st.markdown('# 	:knife_fork_plate: Visão Cuisines')



st.markdown('## Melhores Restaurantes dos Principais tipos Culinários')


cont_metric = st.container()

col1, col2, col3, col4, col5 = cont_metric.columns( 5 )

cuisine = 'Italian'
string_1, string_2 = func_temp(cuisine, df1)
col1.metric(string_1, string_2)
#max_rating_name, max_rating = get_best_restaurant(df1, cuisine)
#col1.metric('Italiana: {}'.format(max_rating_name), '{}/5.0'.format(max_rating))

cuisine = 'American'
max_rating_name, max_rating = get_best_restaurant(df1, cuisine)
col2.metric('Americana: {}'.format(max_rating_name), '{}/5.0'.format(max_rating))

cuisine = 'Arabian'
max_rating_name, max_rating = get_best_restaurant(df1, cuisine)
col3.metric('Árabe: {}'.format(max_rating_name), '{}/5.0'.format(max_rating))

cuisine = 'Japanese'
max_rating_name, max_rating = get_best_restaurant(df1, cuisine)
col4.metric('Japonesa: {}'.format(max_rating_name), '{}/5.0'.format(max_rating))

cuisine = 'Brazilian'
max_rating_name, max_rating = get_best_restaurant(df1, cuisine)
col5.metric('Brasileira: {}'.format(max_rating_name), '{}/5.0'.format(max_rating))


paises_selecionados = df1['country_code'].apply(country_name).isin( countries_selected )
culinarias_selecionadas = df1['cuisines'].isin( cuisines_selected )

linhas_selecionadas = paises_selecionados & culinarias_selecionadas

df2 = df1.copy()
df1 = df1[linhas_selecionadas]


with st.container():
    st.markdown('## Top {} Restaurantes'.format(no_rest_viz))
    
    st.dataframe(df1[['restaurant_id', 'restaurant_name', 'country_code', 'city', 'cuisines', 'average_cost_for_two','aggregate_rating', 'votes']]
                 .sort_values(by='aggregate_rating', ascending=False)
                 .head(no_rest_viz)
                )

    
    
with st.container():
    df2 = df2[paises_selecionados]
    
    df_aux = (df2[['cuisines', 'average_cost_for_two', 'aggregate_rating', 'has_online_delivery']]
                  .groupby(['cuisines']).agg({'average_cost_for_two':'mean', 'aggregate_rating':'mean', 'has_online_delivery':'sum'}).round(2)
                  .reset_index()
             )
    df_aux.columns = ['cuisines', 'mean_average_cost_for_two', 'mean_aggregate_rating', 'sum_has_online_delivery']
    df_aux = df_aux.sort_values(by=['mean_aggregate_rating'], ascending=False)
    #st.dataframe(df_aux)

#-----------------
    
    col1, col2 = st.columns( 2 )
    
    no_couisines_bar = 10
    
    df_aux1 = df_aux.head( no_couisines_bar )
    
    histogram_option_x = 'cuisines'
    histogram_option_y = 'mean_aggregate_rating'
    column_depicted = histogram_option_x
    y_axis = histogram_option_y
    fig = px.bar( df_aux1, x=column_depicted, y=y_axis, title='Melhores {} culinárias registradas'.format( no_couisines_bar ) )
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    fig.update_layout(yaxis_range=[0,5])
    col1.plotly_chart( fig, use_container_width=True )

    
    df_aux2 = df_aux.tail( no_couisines_bar )

    histogram_option_x = 'cuisines'
    histogram_option_y = 'mean_aggregate_rating'
    column_depicted = histogram_option_x
    y_axis = histogram_option_y
    fig = px.bar( df_aux2, x=column_depicted, y=y_axis, title='Piores {} culinárias registradas'.format( no_couisines_bar ) )
    fig.update_layout(xaxis={'categoryorder':'total ascending'})
    fig.update_layout(yaxis_range=[0,5])
    col2.plotly_chart( fig, use_container_width=True )
