# C:\...\aplicacion\pages\1_Dashboard.py (MODIFICADO)

import streamlit as st
import pandas as pd
from dashboard_cientifico.aplicacion.config.settings import CLAVE_DATAFRAME
from dashboard_cientifico.aplicacion.config.config_streamlit import configura_streamlit

from dashboard_cientifico.aplicacion.vista.vista import (lista_meses_cargados,
                                                         grafica_acumulados_dia,
                                                         grafica_queso_provincia)

from dashboard_cientifico.aplicacion.modelo.funciones_graficos import (obtener_acumulados_por_dia_semana,
                                                                       obtener_totales_por_provincia,
                                                                       obtener_max_min_provincia)


def ejecutar_ejercicios(titulo: str, metrica: str, df: pd.DataFrame, meses_cargados: dict):
    st.subheader(titulo)
    st.markdown("##### Gráfico 1: Acumulado por Día de la Semana (Ejercicio 2)")

    opciones_mes = list(meses_cargados.values())
    indice_final_defecto = len(opciones_mes) - 1

    col1, col2 = st.columns(2)
    with col1:
        mes_inicial=st.selectbox(
            label='Mes inicial',
            options=opciones_mes,
            index=0,
            key=f'mes_inicial_{metrica}'
            )
        
    with col2:
        mes_final=st.selectbox(
            label='Mes final',
            options=opciones_mes,
            index=indice_final_defecto,
            key=f'mes_final_{metrica}'
            )

    carga_inicial=None
    carga_final=None
    cargas_a_filtrar: list = []

    for carga_id, mes in meses_cargados.items():
        if mes_inicial== mes:
            carga_inicial=carga_id
        if mes_final== mes:
            carga_final=carga_id

    if carga_inicial is None or carga_final is None:
            cargas_a_filtrar = []
            st.warning(f"Error: No se pudieron encontrar los IDs de carga para los meses.")     
    elif carga_inicial > carga_final:
        st.error("El **'Mes inicial'** debe ser anterior o igual al **'Mes final'**.")
        cargas_a_filtrar = []
    else:
        cargas_a_filtrar = [clave for clave in meses_cargados.keys() if carga_inicial <= clave <= carga_final]

    df_dia = obtener_acumulados_por_dia_semana(df, metrica, cargas_a_filtrar)
    grafica_acumulados_dia(titulo, df_dia, metrica)
    
    st.markdown("---")
    
    st.markdown("##### Gráfico 2: Distribución por Provincia y Análisis Máx/Mín (Ejercicio 3)")

    df_provincia_total = obtener_totales_por_provincia(df, metrica, cargas_a_filtrar)  
    max_min_data = obtener_max_min_provincia(df_provincia_total, metrica)

    configuracion_columnas = {"province": st.column_config.Column("Provincia"),
                              metrica: st.column_config.Column("Total", width="small"),
                              "porcentaje": st.column_config.ProgressColumn(
                                  " % del Total",
                                  format="%.2f %%",
                                  min_value=0,
                                  max_value=100
                                  )
                            }
    
    columnas_a_mostrar = ['province', metrica, 'porcentaje']

    with st.expander("Datos del gráfico (columnas ordenables)", expanded=False):
        st.dataframe(
                df_provincia_total[columnas_a_mostrar],
                hide_index=True,
                column_config=configuracion_columnas
            )    

    grafica_queso_provincia(titulo, df_provincia_total, metrica, max_min_data)


configura_streamlit()
st.title("📊 Dashboard")

if CLAVE_DATAFRAME in st.session_state and not st.session_state[CLAVE_DATAFRAME].empty:
    df: pd.DataFrame = st.session_state[CLAVE_DATAFRAME]
    meses_cargados: dict = lista_meses_cargados(df)

    tab1, tab2, tab3, tab4 = st.tabs(["Defunciones", "Casos", "Hospitalizados", "UCI"])

    with tab1:
        ejecutar_ejercicios('Defunciones','num_def', df, meses_cargados)

    with tab2:
        ejecutar_ejercicios('Casos','new_cases', df, meses_cargados)

    with tab3:
        ejecutar_ejercicios('Hospitalizados','num_hosp', df, meses_cargados)

    with tab4:
        ejecutar_ejercicios('UCI','num_uci', df, meses_cargados)                
else:
    st.warning("Datos no disponibles. Por favor, asegúrate de que la Carga Inicial se ha completado en la página 'Inicio'.")