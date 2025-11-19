from pathlib import Path
import shutil
import pandas as pd
import sqlite3
from ..config.settings import (RUTA_DB,
                               NOMBRE_DB,
                               CARPETA_DB,
                               RUTA_ARCHIVOS,
                               CARPETA_ARCHIVOS,
                               NOMBRE_ARCHIVO_ENTRADA,
                               RUTA_ARCHIVO_ENTRADA,
                               CARPETA_DESCARGAS,
                               RUTA_DESCARGAS,
                               TABLA_IMPORTACION,
                               NOMBRE_JSON,
                               NOMBRE_JSON_ELIMINADOS)


def cargar_datos(archivo_mes_path: Path, carga_id: str) -> str:
    try:
        if not archivo_mes_path.exists():
             raise FileNotFoundError(f"Archivo {archivo_mes_path.name} no encontrado en la ruta.")

        df = pd.read_csv(archivo_mes_path, sep=',', encoding='UTF-8')
        df.columns = df.columns.str.strip()
        
        filas_originales = len(df)

        df['carga_id'] = carga_id

        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce') 
        df.dropna(subset=['date'], inplace=True)
        
        filas_cargadas = len(df)
        filas_omitidas = filas_originales - filas_cargadas

        df['date'] = df['date'].dt.strftime('%d/%m/%Y') 

        db :Path = RUTA_DB / NOMBRE_DB
        conn = sqlite3.connect(db)
        df.to_sql(TABLA_IMPORTACION, conn, if_exists='append', index=False)
        conn.close()

        ruta_cargados: Path = RUTA_ARCHIVOS / "cargados"
        ruta_cargados.mkdir(exist_ok=True)
        nombre_nuevo = f"{archivo_mes_path.stem}_{carga_id}{archivo_mes_path.suffix}"
        ruta_destino: Path = ruta_cargados / nombre_nuevo
        shutil.move(str(archivo_mes_path), str(ruta_destino))
        
        msg = (f"{filas_cargadas} filas válidas para la carga 'carga_id={carga_id}' "
               f"añadidas a '{CARPETA_DB}/{TABLA_IMPORTACION}'.")
        if filas_omitidas > 0:
            msg += f"{filas_omitidas} filas fueron omitidas por fechas inválidas."
        return msg

    except FileNotFoundError as e:
        return f"Error: {e}"
    
    except Exception as e:
        return f"Error durante la carga, transformación o escritura de datos: {e}"



def eliminar_carga_por_id(carga_id: str) -> str:
    """
    Elimina todas las filas de la tabla de importación que coincidan con el carga_id especificado.
    """
    try:
        db: Path = RUTA_DB / NOMBRE_DB
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        # Usamos una consulta parametrizada para prevenir inyección SQL
        query = f"DELETE FROM {TABLA_IMPORTACION} WHERE carga_id = ?"
        
        cursor.execute(query, (carga_id,))
        filas_eliminadas = cursor.rowcount # Obtiene el número de filas afectadas
        
        conn.commit()
        conn.close()
        
        if filas_eliminadas > 0:
            return (f"🗑️ Eliminación exitosa: {filas_eliminadas} filas "
                    f"asociadas al ID '{carga_id}' han sido borradas.")
        else:
            return (f"ℹ️ Aviso: No se encontraron filas con el ID de carga '{carga_id}'.")
            
    except sqlite3.Error as e:
        return f"❌ Error de base de datos al eliminar la carga '{carga_id}': {e}"
    except Exception as e:
        return f"❌ Error inesperado al intentar eliminar la carga '{carga_id}': {e}"
    

def generar_json() -> 'tuple[str, str]':
    datos_exportados_json: str = ""
    datos_eliminados_json: str = ""

    try:
        df = obtener_datos_completos()
        
        if df.empty:
            print("No hay datos en la base de datos para procesar.")
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

        columnas_agrupacion = ['dia_semana', 'province']
        columnas_suma: list = ['num_def', 'new_cases', 'num_hosp', 'num_uci']

        df_agrupado = df.groupby(columnas_agrupacion)[columnas_suma].sum().reset_index()

        datos_json = df_agrupado.to_json(orient='records', indent=4)

        ruta_salida: Path = RUTA_DESCARGAS / NOMBRE_JSON
        
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            f.write(datos_json)

        datos_exportados_json=(f"{len(df_agrupado)} filas de datos agrupados por día/provincia y exportadas a: "
                               f"'{CARPETA_DESCARGAS}/{NOMBRE_JSON}'")

        return datos_eliminados_json, datos_exportados_json
    
    except KeyError as e:
        mensaje_error=(f"Error: Una columna necesaria no fue encontrada. Verifica que las columnas 'date', 'province', {columnas_suma} existan. Detalle: {e}") # type: ignore
        return mensaje_error, mensaje_error
    
    except Exception as e:
        mensaje_error=(f"Error al generar el JSON: {e}")
        return mensaje_error, mensaje_error


def obtener_datos_completos() -> pd.DataFrame:
    try:
        conn = sqlite3.connect(RUTA_DB / NOMBRE_DB)
        query = f"SELECT * FROM {TABLA_IMPORTACION}"

        df = pd.read_sql(query, conn)
        conn.close()
        return df

    except sqlite3.Error as e:
        print(f"Error al consultar la base de datos: {e}")
        return pd.DataFrame()
    
def obtener_archivos_csv() -> list:
    if not RUTA_ARCHIVOS.exists():
        return []
    
    archivos_csv_encontrados = []
    
    for archivo in RUTA_ARCHIVOS.iterdir():
        if archivo.is_file() and archivo.suffix.lower() == '.csv':            
            archivos_csv_encontrados.append(archivo.name)
                
    return archivos_csv_encontrados
    