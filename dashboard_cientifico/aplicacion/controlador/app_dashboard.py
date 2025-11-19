import streamlit as st
from dashboard_cientifico.aplicacion.config.config_streamlit import configura_streamlit
from dashboard_cientifico.aplicacion.vista.vista import introduccion_general
from dashboard_cientifico.aplicacion.modelo.carga_datos import cargar_datos_iniciales, generar_json


configura_streamlit()

st.title("Dashboard Científico")

st.sidebar.title("Menú")

if st.sidebar.button("Cargar datos iniciales", type='primary'):
    cargar_datos_iniciales()
    st.success("Datos iniciales cargados")
    generar_json()

    
pagina=st.sidebar.selectbox("Selecciona página", [
    "Introducción",
    "Configurar semana", 
    "Agrupar"
    ])

introduccion_general()
