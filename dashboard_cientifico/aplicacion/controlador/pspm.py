import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
from typing import List

# ⚠️ Asumimos estas importaciones:
# from dashboard_cientifico.aplicacion.config.settings import CLAVE_DATAFRAME
# from dashboard_cientifico.aplicacion.config.settings import RUTA_DB_COMPLETA # O la ruta que uses


def obtener_cargas_pendientes(df_principal: str, ruta_db: Path) -> List[str]:   
    if df_principal not in st.session_state or st.session_state[df_principal].empty:
        df_principal_cargas = pd.DataFrame()
    else:
        df_principal = st.session_state[df_principal]
        df_principal_cargas = df_principal['carga_id'].unique() 

    try:
        conn = sqlite3.connect(ruta_db)

        df_cargas_id = pd.read_sql_query("SELECT * FROM cargas_id", conn)
        conn.close()

    except sqlite3.Error as e:
        st.error(f"Error al leer la tabla de mapeo de cargas: {e}")
        return []

    if not df_principal_cargas.empty:
        df_pendientes = df_cargas_id[~df_cargas_id['carga_id'].isin(df_principal_cargas)]
    else:
        df_pendientes = df_cargas_id

    cargas_pendientes = [f"{row['mes']}" for index, row in df_pendientes.iterrows()]
    
    return cargas_pendientes

CARGA_ID_POSIBLES=[
                "Mayo 2021 -202105","Junio 2021 -202106",
                "Julio 2021 -202107","Agosto 2021 -202108",
                "Septiembre 2021 -202109","Octubre 2021 -202110",
                "Noviembre 2021 -202111","Diciembre 2021 -202112"
                ]