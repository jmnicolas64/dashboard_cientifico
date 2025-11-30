from pathlib import Path
from typing import Dict, Any, List
import shutil
import os
import pandas as pd
import streamlit as st
import sqlite3
import json
from ..config.settings import (CLAVE_DATAFRAME,
                               RUTA_DB,
                               NOMBRE_DB,
                               CARPETA_DB,
                               RUTA_ARCHIVOS,
                               CARPETA_ARCHIVOS,
                               CARPETA_CARGADOS,
                               RUTA_COPIA_ARCHIVOS,
                               CARPETA_DESCARGAS,
                               RUTA_DESCARGAS,
                               TABLA_DATOS_COVID,
                               TABLA_CARGAS_ID,
                               NOMBRE_JSON_PEDIDO,
                               NOMBRE_JSON_ELIMINADOS,
                               NOMBRE_JSON_CARGAS_ID,
                               )


def inicializar_dataframe():
    df = obtener_datos_completos() 
    
    st.session_state[CLAVE_DATAFRAME] = df
    
    if df.empty:
        st.session_state[CLAVE_DATAFRAME] = pd.DataFrame() 
        return

    df['date'] = pd.to_datetime(df['date'], dayfirst=True)

    df['daily_cases_avg7'] = df.groupby('province')['daily_cases'].transform(
            lambda x: x.rolling(window=7, min_periods=1).mean()
    )

    df['daily_deaths_calculated'] = df.groupby('province')['deceased'].diff().fillna(0)

    df['daily_deaths_avg7'] = df.groupby('province')['daily_deaths_calculated'].transform(
        lambda x: x.rolling(window=7, min_periods=1).mean()
    )
    
    df['cases_per_100k'] = (df['cases_accumulated'] / df['poblacion']) * 100000

    st.session_state[CLAVE_DATAFRAME] = df


def verificar_db() -> Dict[str, Any]:
    ruta_db: Path = RUTA_DB / NOMBRE_DB
    
    estado = {
        "db_existe": False,
        "datos_covid_existe": False,
        "cargas_id_existe": False,
        "final": False
    }

    if not ruta_db.exists():
        estado["final"] = False
        return estado

    estado["db_existe"] = True

    try:
        conn = sqlite3.connect(ruta_db)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas_existentes = [row[0] for row in cursor.fetchall()]

        conn.close()
        
        if TABLA_DATOS_COVID in tablas_existentes:
            estado["datos_covid_existe"] = True
        
        if TABLA_CARGAS_ID in tablas_existentes:
            estado["cargas_id_existe"] = True

        if estado["datos_covid_existe"] and estado["cargas_id_existe"]:
            estado["final"] = True
        else:
            tablas_faltantes = []
            if not estado["datos_covid_existe"]:
                tablas_faltantes.append(f"'{TABLA_DATOS_COVID}'")
            if not estado["cargas_id_existe"]:
                tablas_faltantes.append(f"'{TABLA_CARGAS_ID}'")
            
            estado["final"] = False

    except sqlite3.Error as e:
        estado["final"] = False

    return estado


def reset_datos() -> str:
    mensajes = []

    ruta_db: Path = RUTA_DB / NOMBRE_DB

    try:
        if ruta_db.exists() and ruta_db.is_file():
            os.unlink(ruta_db)
            mensajes.append("DB: Base de datos borrada correctamente.")
        else:
            mensajes.append("DB: Archivo de la base de datos no encontrado, se omite el borrado.")
    
    except Exception as e:
        mensajes.append(f"DB: Error al intentar borrar la base de datos: {e}")
        return "\n\n".join(mensajes) # Detiene la ejecución si falla el borrado de la DB

    try:
        if RUTA_ARCHIVOS.exists():
            shutil.rmtree(RUTA_ARCHIVOS, ignore_errors=True) 
            mensajes.append("DIR: Contenido de la carpeta de entrada borrado.")
            
        RUTA_ARCHIVOS.mkdir(parents=True, exist_ok=False)
        mensajes.append("DIR: Carpeta de entrada recreada y vacía.")

    except Exception as e:
        mensajes.append(f"DIR: Error al borrar/recrear la carpeta de entrada: {e}")
        #return "\n\n".join(mensajes)

    try:
        if not RUTA_COPIA_ARCHIVOS.exists():
            mensajes.append("COPIA: La carpeta de origen de copia no existe. No se copió nada.")
            return "\n\n".join(mensajes)
            
        archivos_copiados = 0
        for item in RUTA_COPIA_ARCHIVOS.iterdir():
            if item.is_file():
                shutil.copy2(item, RUTA_ARCHIVOS / item.name)
                archivos_copiados += 1
        
        mensajes.append(f"COPIA: Se han copiado {archivos_copiados} archivos de respaldo a la carpeta de entrada.")

    except Exception as e:
        mensajes.append(f"COPIA: Error durante el proceso de copia: {e}")

    return "\n\n".join(mensajes)
    

def crear_tabla_carga_ids() -> str:
    try:
        json_cargas_id: Path = RUTA_ARCHIVOS/NOMBRE_JSON_CARGAS_ID

        with open(json_cargas_id, 'r', encoding='utf-8') as f:
            data_dict = json.load(f)
        
        df_cargas = pd.DataFrame(data=list(data_dict.items()), columns=['mes', 'carga_id'])

        db :Path = RUTA_DB / NOMBRE_DB
        conn = sqlite3.connect(db)
        
        df_cargas.to_sql(TABLA_CARGAS_ID, conn, if_exists='replace', index=False)
        
        conn.close()
        
        return (f"La tabla '{NOMBRE_DB}:{TABLA_CARGAS_ID}' ha sido "
                f"creada/reemplazada con {len(df_cargas)} registros de carga.")

    except FileNotFoundError:
        return (f"Error: El archivo json a cargar no fue encontrado en: "
                f"'{CARPETA_ARCHIVOS}/{NOMBRE_JSON_CARGAS_ID}'.")
    
    except json.JSONDecodeError:
        return f"Error: El archivo '{CARPETA_ARCHIVOS}/{NOMBRE_JSON_CARGAS_ID}' contiene JSON inválido."
    
    except sqlite3.Error as e:
        return f"Error de base de datos al crear la tabla '{NOMBRE_DB}:{TABLA_CARGAS_ID}': {e}"
    
    except Exception as e:
        return f"Error inesperado: {e}"


def cargar_datos(archivo_mes_path: Path, carga_id: str, mes: str) -> str:
    try:
        if not archivo_mes_path.exists():
             raise FileNotFoundError(f"Archivo {archivo_mes_path.name} no encontrado en la ruta.")

        df = pd.read_csv(archivo_mes_path, sep=',', encoding='UTF-8')
        df.columns = df.columns.str.strip()
        
        filas_originales = len(df)

        df['carga_id'] = carga_id
        df['mes'] = ""

        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce') 
        df.dropna(subset=['date'], inplace=True)
        
        filas_cargadas = len(df)
        filas_omitidas = filas_originales - filas_cargadas

        df['date'] = df['date'].dt.strftime('%d/%m/%Y') 

        db :Path = RUTA_DB / NOMBRE_DB
        conn = sqlite3.connect(db)
        cursor=conn.cursor()

        query = f"SELECT mes FROM {TABLA_CARGAS_ID} WHERE carga_id='{carga_id}'"
        cursor.execute(query)
        mes = cursor.fetchone()[0]
        df['mes'] = mes

        df.to_sql(TABLA_DATOS_COVID, conn, if_exists='append', index=False)

        conn.close()

        ruta_cargados: Path = RUTA_ARCHIVOS / "cargados"
        ruta_cargados.mkdir(exist_ok=True)
        nombre_nuevo = f"{archivo_mes_path.stem}_{carga_id}{archivo_mes_path.suffix}"
        ruta_destino: Path = ruta_cargados / nombre_nuevo
        shutil.move(str(archivo_mes_path), str(ruta_destino))
        
        msg = (f"CARGA: {filas_cargadas} filas válidas del mes '{mes}' "
               f"añadidas a '{CARPETA_DB}/{TABLA_DATOS_COVID}'.")
        if filas_omitidas > 0:
            msg += f"{filas_omitidas} filas fueron omitidas por fechas inválidas."
        return msg

    except FileNotFoundError as e:
        return f"Error: {e}"
    
    except Exception as e:
        return f"Error: durante la carga, transformación o escritura de datos: {e}"


def generar_json() -> tuple[str, str]:
    datos_exportados_json: str = ""
    datos_eliminados_json: str = ""

    try:
        df = obtener_datos_completos()
        
        if df.empty:
            st.warning("No hay datos en la base de datos para procesar.")
            return datos_eliminados_json, datos_exportados_json

        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y', errors='coerce') 
        df_eliminados = df[df['date'].isnull()].copy()

        if not df_eliminados.empty:
            ruta_log: Path = RUTA_DESCARGAS / NOMBRE_JSON_ELIMINADOS
            datos_eliminados = df_eliminados.to_json(orient='records', indent=4)
            
            with open(ruta_log, 'w', encoding='utf-8') as archivo_json:
                archivo_json.write(datos_eliminados)
                
            datos_eliminados_json=(f"{len(df_eliminados)} filas con fechas inválidas exportadas a: "
                                   f"{CARPETA_DESCARGAS}/{NOMBRE_JSON_ELIMINADOS}")

        df.dropna(subset=['date'], inplace=True)

        df['dia_semana'] = df['date'].dt.strftime('%A')

        columnas_agrupacion = ['carga_id','dia_semana', 'province']
        columnas_suma: list = ['num_def', 'new_cases', 'num_hosp', 'num_uci']

        df_agrupado = df.groupby(columnas_agrupacion)[columnas_suma].sum().reset_index()

        datos_json = df_agrupado.to_json(orient='records', indent=4)

        ruta_salida: Path = RUTA_DESCARGAS / NOMBRE_JSON_PEDIDO
        
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            f.write(datos_json)

        datos_exportados_json=(f"{len(df_agrupado)} filas de datos agrupados por día/provincia y exportadas a: "
                               f"'{CARPETA_DESCARGAS}/{NOMBRE_JSON_PEDIDO}'")

        return datos_eliminados_json, datos_exportados_json
    
    except KeyError as e:
        mensaje_error=(f"Error: Una columna necesaria no fue encontrada. Verifica que las columnas 'date', 'province', {columnas_suma} existan. Detalle: {e}") # type: ignore
        return mensaje_error, mensaje_error
    
    except Exception as e:
        mensaje_error=(f"Error al generar el JSON: {e}")
        return mensaje_error, mensaje_error


def eliminar_carga(carga_id: str, mes: str) -> str:
    conn=None
    try:
        db: Path = RUTA_DB / NOMBRE_DB
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        query = f"DELETE FROM {TABLA_DATOS_COVID} WHERE carga_id = ?"
        
        cursor.execute(query, (carga_id,))
        filas_eliminadas = cursor.rowcount
        
        conn.commit()
        
        if filas_eliminadas > 0:
            RUTA_CARGADOS: Path= RUTA_ARCHIVOS / CARPETA_CARGADOS
            busca_str = f"*{carga_id}*"
            archivos_encontrados = list(RUTA_CARGADOS.glob(busca_str))

            if archivos_encontrados:
                archivo_a_mover = archivos_encontrados[0]
                nombre_archivo=archivo_a_mover.name
                quitar_del_nombre = f"_{carga_id}"
                nombre_original = nombre_archivo.replace(quitar_del_nombre, '')

                ruta_final = RUTA_ARCHIVOS / nombre_original
                
                shutil.move(str(archivo_a_mover), str(ruta_final))

            return (f"Eliminación exitosa: {filas_eliminadas} filas "
                    f"asociadas al mes '{mes}' han sido borradas.")
        else:
            return (f"Aviso: No se encontraron filas con el mes '{mes}'.")
            
    except sqlite3.Error as e:
        return f"Error: de base de datos al eliminar la carga '{carga_id}': {e}"
    
    except Exception as e:
        return f"Error: inesperado al intentar eliminar la carga '{carga_id}': {e}"
    
    finally:
        if conn:
            conn.close()
    

def obtener_datos_completos() -> pd.DataFrame:
    try:
        conn = sqlite3.connect(RUTA_DB / NOMBRE_DB)
        query = f"SELECT * FROM {TABLA_DATOS_COVID}"

        df = pd.read_sql(query, conn)
        conn.close()

    except sqlite3.Error as e:
        st.error(f"Error al consultar la base de datos: {e}")
        return pd.DataFrame()

    columnas_a_eliminar = [
        'source_name', 
        'source',
        'comments'
    ]
    
    df = df.drop(
        columns=columnas_a_eliminar, 
        axis=1, 
        errors='ignore'
    )
    
    return df


def obtener_archivos_csv() -> list:
    if not RUTA_ARCHIVOS.exists():
        return []
    
    archivos_csv_encontrados = []

    for archivo in RUTA_ARCHIVOS.iterdir():
        if archivo.is_file() and archivo.suffix.lower() == '.csv':
            archivos_csv_encontrados.append(archivo.name)
                
    return archivos_csv_encontrados


def obtener_cargas_pendientes(s_principal_cargas: pd.Series) -> List[str]:
    db: Path=RUTA_DB / NOMBRE_DB
    conn = sqlite3.connect(db)

    df_cargas_id = pd.read_sql_query("SELECT * FROM cargas_id ORDER BY carga_id", conn)
    conn.close()

    if not s_principal_cargas.empty:
        df_pendientes = df_cargas_id[~df_cargas_id['carga_id'].isin(s_principal_cargas)]
    else:
        df_pendientes = df_cargas_id

    cargas_pendientes = [f"{row['mes']}" for index, row in df_pendientes.iterrows()]

    return cargas_pendientes


def dame_carga_id_mes(mes_seleccionado: str) ->str:
    db: Path = RUTA_DB / NOMBRE_DB

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    query = "SELECT carga_id FROM cargas_id WHERE mes = ?"

    cursor.execute(query, (mes_seleccionado,))
    resultado = cursor.fetchone()
   
    conn.close()

    return str(resultado[0])