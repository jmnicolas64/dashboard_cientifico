import streamlit as st
from dashboard_cientifico.aplicacion.config.config_streamlit import configura_streamlit
from dashboard_cientifico.aplicacion.vista.vista import introduccion_general


configura_streamlit()

st.title("Dashboard Científico")

st.sidebar.title("Menú")

if st.sidebar.button("Cargar excel original", type='primary'):
    #cargar_limpiar_excel()
    st.success("Excel cargado")   
    
pagina=st.sidebar.selectbox("Selecciona página", [
    "Introducción",
    "Configurar semana", 
    "Agrupar"
    ])

introduccion_general()