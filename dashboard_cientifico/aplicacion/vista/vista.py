import streamlit as st
import pandas as pd
import plotly.express as px
from typing import Dict, List
from dashboard_cientifico.aplicacion.modelo.carga_datos import obtener_meses_disponibles


def introduccion_general():
    st.title("Bienvenido al Dashboard Científico")
    
    with st.expander("C o m e n t a r i o s", expanded=False, width='stretch'):
        st.markdown("""
                
                ### Contexto del Desarrollo
                
                Este dashboard científico fue creado como parte de un proyecto educativo, centrándose en la **arquitectura MVC (Modelo-Vista-Controlador)** para mantener la separación de responsabilidades:
                
                * **Modelo:** Lógica de datos (Pandas, SQLite).
                * **Vista:** Funciones de dibujo (Plotly, Streamlit).
                * **Controlador:** Flujo principal de las páginas.
                
                

        [Image of a software architecture diagram showing MVC]

                
                **Fuentes de Datos:** Los datos provienen del Ministerio de Sanidad, Consumo y Bienestar Social de España, con un enfoque en la segunda mitad del año 2021.
                
                *Recordatorio: Utiliza la sección 'Gestión' para cargar o restablecer los datos.*
                
                """, unsafe_allow_html=False)

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


def lista_meses_cargados(df: pd.DataFrame) -> Dict:
    st.sidebar.markdown("#### Datos disponibles")
    meses_disponibles: Dict = obtener_meses_disponibles(df)
    if meses_disponibles and "Error" in meses_disponibles.get(1, ''):
        st.sidebar.error(meses_disponibles.get(1))
    
    
            
    lista_formateada = "\n".join([f"- {mes}" for mes in meses_disponibles.values()])
    
    # 3. Dibujar la lista en la barra lateral usando st.markdown
    st.sidebar.markdown(lista_formateada)

    return meses_disponibles
    

def grafica_acumulados_dia(titulo: str, df_dia: pd.DataFrame, metrica: str):
    fig = px.bar(
        df_dia,
        x='dia_semana',
        y=metrica,
        title=f"Total Acumulado de {titulo} por Día de la Semana",
        labels={'dia_semana': 'Día de la Semana ', metrica: f'Total Acumulado ({titulo}) '},
        color=metrica,
        color_continuous_scale=px.colors.sequential.Teal,
        template='plotly_white'
    )
    st.plotly_chart(fig, width='stretch')


def grafica_queso_provincia(titulo: str, df_provincia_total: pd.DataFrame, metrica: str, max_min_data: Dict):
    fig = px.pie(
        df_provincia_total,
        values=metrica,
        names='province',
        title=(f"Distribución Total de {titulo} por Provincia"),
        hole=0.3,
        template='plotly_white'
    )

    fig.update_layout( 
        height=500,
        margin=dict(t=50, b=50, l=10, r=10)
    )

    fig.update_traces(
        textinfo='none',
        hoverinfo='skip',
        hovertemplate=(
            "<b>Provincia:</b> %{label}<br>" +
            "<b>Total:</b> %{value:,.0f} Uds.<br>" +
            "<b>Porcentaje:</b> %{percent}<extra></extra>"
            )
        )

    st.plotly_chart(fig, config={'displayModeBar': False})
    
    st.markdown(f"""
    <div style="background-color: #ECF0F1; padding: 15px; border-radius: 5px; margin-top: 10px;">
        <strong>Resultados del Análisis de {titulo}:</strong>
        <ul>
            <li>Provincia con valor MÁXIMO: {max_min_data['max_provincia']} (Total: {max_min_data['max_valor']:,})</li>
            <li>Provincia con valor MÍNIMO: {max_min_data['min_provincia']} (Total: {max_min_data['min_valor']:,})</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


def grafico_evolucion_mensual(df_evolucion: pd.DataFrame, metrica: str, titulo: str):
    titulo_grafico=f"Evolución Mensual de {titulo}"
    fig = px.line(
        df_evolucion,
        x="date",
        y=metrica,
        title=titulo_grafico,
        height=500
    )
    
    fig.update_layout(
        xaxis_title="Mes", 
        yaxis_title=titulo,
        title_x=0.5
    )

    ultima_fecha = df_evolucion['date'].max()
    rango_x_fin = ultima_fecha + pd.DateOffset(days=10)
    primera_fecha = df_evolucion['date'].min()

    fig.update_xaxes(
            range=[primera_fecha, rango_x_fin],
            showticklabels=True, 
            tickangle=45,
            dtick="M1", 
            tickformat="%b %Y" 
        )
    
    min_val = df_evolucion[metrica].min()
    max_val = df_evolucion[metrica].max()

    margen = (max_val - min_val)
    margen = margen * 0.05 if margen > 0 else max_val * 0.1

    y_range_min = max(0, min_val - margen)
    y_range_max = max_val + margen

    fig.update_yaxes(
        range=[y_range_min, y_range_max],
        zeroline=True, 
        zerolinewidth=1, 
        zerolinecolor='lightgray'
    )

    st.plotly_chart(fig, width='stretch')


def grafico_distribucion(df_original: pd.DataFrame, metrica_clave: str, metrica_nombre_legible: str):
    """
        [VISTA] Dibuja un Gráfico de Caja donde cada caja representa la distribución de
        los valores DIARIOS dentro de cada mes de la serie temporal.
        """
    df_plot = df_original.copy()
    
    # 1. Crear una columna para etiquetar los meses (ej. "Ene 2021")
    # Es crucial que la columna 'date' sea de tipo datetime antes de esto
    df_plot['Mes-Año'] = df_plot['date'].dt.strftime('%b %Y') # type: ignore

    # 2. Ordenar las categorías del eje X cronológicamente
    # Plotly necesita la lista de categorías ordenadas para que no las ordene alfabéticamente
    orden_meses = df_plot.sort_values(by='date')['Mes-Año'].unique().tolist()
    
    limite_superior_y = df_plot[metrica_clave].quantile(0.95)
    limite_superior_y = int(limite_superior_y * 1.1) # Añadimos un 10% de margen y lo convertimos a entero
    if limite_superior_y == 0:
        limite_superior_y = df_plot[metrica_clave].max() # Si el 95% es cero, usamos el máximo

    fig = px.violin(
        df_plot,
        x='Mes-Año', # El eje X es el Mes-Año (categoría)
        y=metrica_clave, # El eje Y es el valor DIARIO de la métrica
        color='Mes-Año',
        title=f'Distribución Diaria de {metrica_nombre_legible} por Mes',
        height=550,
        labels={metrica_clave: metrica_nombre_legible, 'Mes-Año': 'Mes'},
        category_orders={'Mes-Año': orden_meses}, # Asegura el orden cronológico
        box=True, # Muestra el box plot y la mediana dentro del violín
        points='all' # Desactivamos la visualización de todos los puntos para la densidad, es más limpio        
    )
    
    fig.update_layout(
        xaxis_title="Mes", 
        yaxis_title=metrica_nombre_legible,
        title_x=0.5
    )
    
    fig.update_yaxes(
            range=[0, limite_superior_y], 
            title=metrica_nombre_legible
        )


    fig.update_xaxes(tickangle=45)

    st.plotly_chart(fig, width='stretch')


def grafico_correlacion(matriz_corr: pd.DataFrame, metricas_nombres: dict):
    """
    [VISTA] Dibuja un Mapa de Calor de la matriz de correlación.
    """
    # Usar los nombres legibles de las métricas en la matriz
    matriz_corr = matriz_corr.rename(columns=metricas_nombres, index=metricas_nombres)
    
    fig = px.imshow(
        matriz_corr,
        text_auto=".2f", # type: ignore 
        color_continuous_scale=px.colors.diverging.RdBu, # Escala de color Rojo-Azul
        color_continuous_midpoint=0, # El punto medio (correlación 0) es blanco
        title="Correlación Mensual de Métricas de la Pandemia",
        aspect="equal"
    )
    
    fig.update_xaxes(side="top") # Etiquetas del eje X en la parte superior
    
    st.plotly_chart(fig, width='stretch')

