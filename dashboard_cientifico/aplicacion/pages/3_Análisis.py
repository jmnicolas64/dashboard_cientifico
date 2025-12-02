import streamlit as st
import pandas as pd
import plotly.express as px
from dashboard_cientifico.aplicacion.config.settings import CLAVE_DATAFRAME
from dashboard_cientifico.aplicacion.config.config_streamlit import configura_streamlit

from dashboard_cientifico.aplicacion.modelo.funciones_graficos import (obtener_datos_agrupados,
                                                                       obtener_evolucion_nacional,
                                                                       obtener_ia14_por_ccaa,
                                                                       obtener_evolucion_mensual)

from dashboard_cientifico.aplicacion.vista.vista import (lista_meses_cargados,
                                                         grafico_evolucion_mensual)

METRICAS_ANALISIS = {
    "num_def": "Defunciones",
    "new_cases": "Casos",
    "num_hosp": "Hospitalizados",
    "num_uci": "UCI"
}


# =========================================================================
# FLUJO PRINCIPAL (Controlador)
# =========================================================================


configura_streamlit()
st.title("🔬 Análisis Detallado de Datos")

if CLAVE_DATAFRAME in st.session_state and not st.session_state[CLAVE_DATAFRAME].empty:
    df: pd.DataFrame = st.session_state[CLAVE_DATAFRAME]
    lista_meses_cargados(df)
       
    tab1, tab2 = st.tabs(['Evolución', 'Otros'])

    with tab1:
        tab_titles = list(METRICAS_ANALISIS.values())
        tabs = st.tabs(tab_titles)
        
        for i, (col_key, tab_title) in enumerate(METRICAS_ANALISIS.items()):
            with tabs[i]:
                try:
                    df_evolucion = obtener_evolucion_mensual(df, col_key)
                    
                    grafico_evolucion_mensual(
                        df_evolucion, 
                        col_key,
                        tab_title
                    )

                    df_presentacion = df_evolucion.copy()
                    df_presentacion['date'] = df_presentacion['date'].dt.strftime('%m/%Y') # type: ignore
                    df_presentacion.rename(columns={'date': 'Fecha',
                                                    col_key: tab_title
                                                    }, inplace=True)

                    with st.expander("Datos del gráfico", expanded=False):
                        st.dataframe(df_presentacion, width='stretch')

                except Exception as e:
                    st.error("No hay datos para generar el análisis de evolución para " + tab_title + ".")

                

    with tab2:
        tabs1, tabs2, tabs3, tabs4=st.tabs(["Agrupación y Agregación", "Filtrado Rápido", "Evolución Temporal Nacional", "Análisis Geográfico (IA14)"])
        with tabs1:
            pass

        with tabs2:
            pass
        
        with tabs3:
            pass

        with tabs4:
            pass
else:
    st.warning("Datos no disponibles. Por favor, asegúrate de que la Carga Inicial se ha completado en la página 'Inicio'.")
