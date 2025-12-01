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
                    /* 1. Estilo para el Contenedor Principal (Bloqueado) */
                    .block-container {
                        padding-top: 1.5rem;
                        padding-bottom: 1.5rem;
                        padding-left: 5rem;
                        padding-right: 5rem;
                    }
                
                    [data-testid="stSidebar"] {
                        background-color: white !important; /* Fondo blanco */
                    }
                
                    /* --------------------------------------------------------------------------------------- */
                    /* 2. Estilo para todos los enlaces de la navegación lateral (TEXTO y TAMAÑO)               */
                    /* Se usa !important y un selector más específico para anular la regla interna de Streamlit */
                    /* --------------------------------------------------------------------------------------- */
                    [data-testid="stSidebarNav"] li > a {
                        color: #17202A; 
                        font-weight: 500; 
                        margin-bottom: 0.5rem; 
                    }
                    
                    /* Selector para aplicar tamaño al texto interno del enlace (Asegura la anulación) */
                    [data-testid="stSidebarNav"] li > a * {
                        font-size: 1em !important; /* <--- USAR !important AQUÍ */
                    }

                    /* 3. Estilo para el enlace seleccionado (página activa) */
                    [data-testid="stSidebarNav"] li > a[aria-current="page"] {
                        color: white; 
                        background-color: #3498DB;
                        border-radius: 5px; 
                        font-weight: bold;
                    }

                    /* 4. Estilo al pasar el ratón por encima (hover) */
                    [data-testid="stSidebarNav"] li > a:hover {
                        color: #3498DB; 
                        background-color: #ECF0F1; 
                    }
                </style>
                """, unsafe_allow_html=True)                

    

def configura_streamlit():
    configura_locale()
    configura_logo_estilos()

