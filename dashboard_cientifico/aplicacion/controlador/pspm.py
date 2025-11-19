import streamlit as st
import pandas as pd
from pathlib import Path
import os
import sqlite3

# Importamos las funciones del módulo de modelo (asumimos que está en carga_datos_model.py)
# from aplicacion.modelo.carga_datos_model import cargar_datos

# --- CONFIGURACIÓN Y CONSTANTES (AJUSTE ESTAS RUTAS) ---
# Usamos una ruta de ejemplo para la carpeta que contiene los CSVs a cargar
RUTA_ARCHIVOS_ENTRADA = Path(r"C:\Users\josem\Documents\Cursos\Deusto_Python\Proyecto_Final\dashboard_cientifico\archivos")

# Opciones de Load ID que usted necesita (ejemplo)
LOAD_ID_OPTIONS = ["Mayo_2021_Carga1", "Mayo_2021_Carga2", "Junio_2021", "Julio_2021", "Agosto_2021"]


def obtener_archivos_csv(directorio: Path) -> list:
    """Devuelve una lista de nombres de archivos CSV en el directorio."""
    # Filtramos por archivos que terminan en .csv (ignorando mayúsculas/minúsculas)
    if not directorio.exists():
        return []
    
    return [f.name for f in directorio.iterdir() if f.is_file() and f.suffix.lower() == '.csv']


def dashboard_app():
    """Estructura principal de la aplicación Streamlit."""
    st.set_page_config(layout="wide")
    st.title("📊 Dashboard Científico de Datos COVID")

    # --- BARRA LATERAL (Sidebar) ---
    st.sidebar.header("🛠️ Gestión de Datos")
    
    # 1. SECCIÓN DE CARGA DE DATOS
    st.sidebar.subheader("📤 Cargar Nuevo CSV")
    
    # Obtener archivos CSV disponibles
    archivos_disponibles = obtener_archivos_csv(RUTA_ARCHIVOS_ENTRADA)

    if not archivos_disponibles:
        st.sidebar.warning(f"No se encontraron archivos CSV en la ruta: {RUTA_ARCHIVOS_ENTRADA}")
        archivo_seleccionado = None
        load_id_seleccionado = None
    else:
        # Desplegable para seleccionar archivo
        archivo_seleccionado = st.sidebar.selectbox(
            "Seleccione el archivo a cargar:",
            archivos_disponibles
        )

        # Desplegable para seleccionar Load ID
        load_id_seleccionado = st.sidebar.selectbox(
            "Seleccione el ID de Carga:",
            LOAD_ID_OPTIONS
        )

        # Botón para iniciar la carga
        if st.sidebar.button("🚀 Iniciar Carga de Datos"):
            if archivo_seleccionado and load_id_seleccionado:
                # Construir la ruta completa del archivo
                ruta_completa_archivo = RUTA_ARCHIVOS_ENTRADA / archivo_seleccionado
                
                # Ejecutar la función de carga (Asumimos que cargar_datos está disponible)
                # NOTA: Descomentar la línea de importación al inicio para que esto funcione
                try:
                    # Llamada a la función del modelo
                    # resultado = cargar_datos(ruta_completa_archivo, load_id_seleccionado)
                    
                    # Usamos un placeholder de resultado para probar la UI
                    resultado = f"✅ PLACEHOLDER: Carga '{load_id_seleccionado}' exitosa de {archivo_seleccionado}."
                    
                    # Mostrar el resultado al usuario
                    if "❌ Error" in resultado:
                        st.error(resultado)
                    else:
                        st.success(resultado)
                        
                    # ⚠️ IMPORTANTE: Si la carga es exitosa, es bueno recargar la lista de archivos
                    # para que el archivo recién movido desaparezca de la lista
                    st.experimental_rerun() 

                except NameError:
                    st.error("❌ Error: La función 'cargar_datos' no está disponible. Verifique las importaciones.")

    
    # --- CONTENIDO PRINCIPAL (Donde se mostrarían los gráficos) ---
    st.header("Análisis de Datos Agrupados")
    st.info("Utilice la barra lateral para gestionar la carga de datos o ver el análisis.")
    
    # Aquí iría el código para mostrar el JSON agrupado generado por generar_json()
    # st.subheader("Resumen de la Base de Datos")
    # try:
    #     df_db = obtener_datos_completos()
    #     st.dataframe(df_db.tail())
    # except:
    #     st.warning("No hay datos cargados en la base de datos.")


if __name__ == '__main__':
    dashboard_app()