import locale
import streamlit as st

from ..config.settings import RUTA_IMAGENES

def configura_locale():
    try:
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, 'es')
        except locale.Error:
            st.warning("No se pudo establecer la configuración regional a español.")


def configura_logo_estilos():
    st.set_page_config(
        page_title="Dashboard Científico",
        page_icon=f"{RUTA_IMAGENES}/logo.jpg",
        layout="wide",
        initial_sidebar_state="expanded"
)    
    st.logo(f"{RUTA_IMAGENES}/logo.jpg",size="large")
    
    st.markdown("""
                <style>
                    .block-container {
                        padding-top: 1rem; # Ajusta este valor (ej: 0rem, 0.5rem)
                        padding-bottom: 0rem;
                        padding-left: 5rem;
                        padding-right: 5rem;
                    }
                </style>
                """, unsafe_allow_html=True)
    

def configura_streamlit():
    configura_locale()
    configura_logo_estilos()

