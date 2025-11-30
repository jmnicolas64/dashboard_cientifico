import streamlit as st
import pandas as pd
import plotly.express as px
from typing import Dict
from dashboard_cientifico.aplicacion.modelo.carga_datos import obtener_meses_disponibles

def introduccion_general():
    st.title("Bienvenido al Dashboard Científico")
    st.subheader("Menú principal")
    st.markdown(
    """
    Selecciona una opción en el menú lateral:
    <ul>
        <li><span style="font-family: 'Calibri', sans-serif; font-size: 1.1em;">Dashboard</span></li>
        <li><span style="font-family: 'Calibri', sans-serif; font-size: 1.1em;">Análisis</span></li>
        <li><span style="font-family: 'Calibri', sans-serif; font-size: 1.1em;">Datos</span></li>
        <li><span style="font-family: 'Calibri', sans-serif; font-size: 1.1em;">Gestión</span></li>
    </ul>
    """,
    unsafe_allow_html=True)


def introduccion_inicial():
    st.header("Bienvenidos al Dashboard sobre los datos de Covid en la segunda mitad del año 2021")
    st.subheader("Carga de datos")
    st.markdown(
    """
    Esta pagína aparece cuando no hay datos disponibles en la base de datos:
    <ul>
        <li><span style="font-family: 'Calibri', sans-serif; font-size: 1.1em;">Porque es la carga inicial</span></li>
        <li><span style="font-family: 'Calibri', sans-serif; font-size: 1.1em;">Porque se ha borrado accidentalmente la base de datos</span></li>
        <li><span style="font-family: 'Calibri', sans-serif; font-size: 1.1em;">Porque se ha elegido la opción 'Reset datos' del menú 'Gestión de Datos' (en el siguiente menú)</li>
    </ul>

    <div style="font-size: 1.2em; color: #333333; margin-top: 15px; margin-bottom: 15px;">
        <b>Seleccionar en el menú lateral 'Carga inicial' y pulsar el botón 'Cargar datos'</b>
    </div>

    <p>Aparecera a continuación la información del proceso</p>
   
    """,
    unsafe_allow_html=True)


def mostrar_mensajes_y_continuar(clave_num, clave_del, clave_exp, clave_terminada: str):
    
    num_f = st.session_state.get(clave_num, "")
    datos_d = st.session_state.get(clave_del, "")
    datos_e = st.session_state.get(clave_exp, "")
    
    mensaje_mostrado = False
    
    if num_f:
        st.success(num_f)
        mensaje_mostrado = True
    if datos_e:
        st.success(datos_e)
        mensaje_mostrado = True
    if datos_d:
        st.warning(datos_d)
        mensaje_mostrado = True
        
    if mensaje_mostrado:
        st.session_state[clave_num] = ""
        st.session_state[clave_del] = ""
        st.session_state[clave_exp] = ""

        if st.session_state.get(clave_terminada, False):
            st.session_state[clave_terminada] = False
            st.session_state['menu_refresh_key'] += 1
            st.rerun()


def mostrar_mensaje_con_continuacion(clave_mensaje: str, clave_terminada: str): 
    mensaje = st.session_state.get(clave_mensaje, "")
    
    if mensaje:
        if "Aviso:" in mensaje:
            st.warning(mensaje)
        elif "Error:" in mensaje:
            st.error(mensaje)
        else:
            st.success(mensaje)
        
        st.session_state[clave_mensaje] = "" 
        
        # 3. Lógica de Rerun (Control de Flujo)
        # Esto reemplaza el botón "Continuar..."
        if st.session_state.get(clave_terminada, False):
            st.session_state[clave_terminada] = False # Limpiamos la bandera de terminado
            st.session_state['menu_refresh_key'] += 1
            st.rerun()


def lista_meses_cargados(df: pd.DataFrame):
    st.sidebar.markdown("#### Meses Cargados")
    meses_disponibles = obtener_meses_disponibles(df)
    if meses_disponibles and "Error" in meses_disponibles[0]:
        st.sidebar.error(meses_disponibles[0])
        return
            
    lista_formateada = "\n".join([f"- {mes}" for mes in meses_disponibles])
    
    # 3. Dibujar la lista en la barra lateral usando st.markdown
    st.sidebar.markdown(lista_formateada)
    
# dashboard_cientifico/aplicacion/vista/vista.py (Añadir estas funciones)

# --------------------------------------------------------------------------
# EJERCICIO 2: Gráfica de Barras (Acumulado por Día de la Semana)
# --------------------------------------------------------------------------

def dibujar_grafica_acumulados_dia(df_dia: pd.DataFrame, metrica: str):
    titulo_metrica = metrica.replace('_', ' ').title()

    fig = px.bar(
        df_dia,
        x='day_of_week',
        y=metrica,
        title=f"Total Acumulado de {titulo_metrica} por Día de la Semana",
        labels={'day_of_week': 'Día de la Semana', metrica: f'Total Acumulado ({titulo_metrica})'},
        color=metrica,
        color_continuous_scale=px.colors.sequential.Teal,
        template='plotly_white'
    )
    st.plotly_chart(fig, width='stretch')

# --------------------------------------------------------------------------
# EJERCICIO 3: Gráfica de Queso (Distribución por Provincia + Máx/Mín)
# --------------------------------------------------------------------------

def dibujar_grafica_queso_provincia(df_provincia_total: pd.DataFrame, metrica: str, max_min_data: Dict):
    titulo_metrica = metrica.replace('_', ' ').title()

    fig = px.pie(
        df_provincia_total,
        values=metrica,
        names='province',
        title=f"Distribución Total de {titulo_metrica} por Provincia",
        hole=0.3, # Gráfica de "donut"
        template='plotly_white'
    )

    fig.update_layout(
        height=650, 
        margin=dict(t=50, b=50, l=10, r=10) # Reducir márgenes externos para más espacio
    )

    fig.update_traces(textinfo='none')

    st.plotly_chart(fig, use_container_width=True)
    
    # Mostrar máximo y mínimo (Requisito de Ejercicio 3)
    # Se añade formato de miles (:,) para los valores
    st.markdown(f"""
    <div style="background-color: #ECF0F1; padding: 15px; border-radius: 5px; margin-top: 10px;">
    **Resultados del Análisis de {titulo_metrica}:**<br><br>
    * **Provincia con MÁXIMO:** **{max_min_data['max_provincia']}** (Total: {max_min_data['max_valor']:,})<br>
    * **Provincia con MÍNIMO:** **{max_min_data['min_provincia']}** (Total: {max_min_data['min_valor']:,})<br>
    </div>
    """, unsafe_allow_html=True)
