from pathlib import Path
import sys
import pandas as pd
import sqlite3
from ..config.settings import (RUTA_DB,
                               NOMBRE_DB,
                               RUTA_ARCHIVOS,
                               CARPETA_ARCHIVOS,
                               NOMBRE_ARCHIVO_ENTRADA,
                               RUTA_ARCHIVO_ENTRADA,
                               CARPETA_DESCARGAS,
                               RUTA_DESCARGAS,
                               TABLA_IMPORTACION,
                               NOMBRE_JSON,
                               NOMBRE_JSON_ELIMINADOS)


def cargar_datos_iniciales() -> None:  
    try:
        #print(f"⏳ Cargando datos desde {CARPETA_ARCHIVOS}/{NOMBRE_ARCHIVO_ENTRADA} e insertando en SQLite...")
        
        if not RUTA_ARCHIVO_ENTRADA.exists():
             raise FileNotFoundError(f"Archivo {CARPETA_ARCHIVOS}/{NOMBRE_ARCHIVO_ENTRADA} no encontrado.")

        # Carga del CSV
        df = pd.read_csv(RUTA_ARCHIVO_ENTRADA, sep=',', encoding='UTF-8')
        df.columns = df.columns.str.strip()
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        df['date'] = df['date'].dt.strftime('%d/%m/%Y')

        # 1. Conexión a la DB
        db :Path = RUTA_DB / NOMBRE_DB
        conn = sqlite3.connect(db)
        
        # 2. Escritura: Usamos if_exists='replace' para borrar y recrear la tabla
        df.to_sql(TABLA_IMPORTACION, conn, if_exists='replace', index=False)
        
        conn.close()
        #print(f"🎉 Datos cargados exitosamente. La tabla '{TABLA_IMPORTACION}' ha sido reemplazada en: {RUTA_DB}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error durante la carga, transformación o escritura de datos: {e}")
        sys.exit(1)



def generar_json() -> None:
    try:
        df = obtener_datos_completos()
        
        if df.empty:
            print("No hay datos en la base de datos para procesar.")
            return

        df['date'] = pd.to_datetime(df['date'], errors='coerce') 
        df_eliminados = df[df['date'].isnull()].copy()

        if not df_eliminados.empty:
            ruta_log: Path = RUTA_DESCARGAS / NOMBRE_JSON_ELIMINADOS
            datos_eliminados_json = df_eliminados.to_json(orient='records', indent=4)
            
            with open(ruta_log, 'w', encoding='utf-8') as archivo_json:
                archivo_json.write(datos_eliminados_json)
                
            print(f"{len(df_eliminados)} filas con fechas inválidas exportadas a: {CARPETA_DESCARGAS}/{NOMBRE_JSON_ELIMINADOS}")

        df.dropna(subset=['date'], inplace=True)

        df['dia_semana'] = df['date'].dt.strftime('%A')

        columnas_agrupacion = ['dia_semana', 'province']
        columnas_suma: list = ['num_def', 'new_cases', 'num_hosp', 'num_uci']

        df_agrupado = df.groupby(columnas_agrupacion)[columnas_suma].sum().reset_index()

        datos_json = df_agrupado.to_json(orient='records', indent=4)

        ruta_salida: Path = RUTA_DESCARGAS / NOMBRE_JSON
        
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            f.write(datos_json)

        print(f"Datos agrupados por día/provincia y guardados en: {ruta_salida}")
    
    except KeyError as e:
        print(f"Error: Una columna necesaria no fue encontrada. Verifica que las columnas 'date', 'province', {columnas_suma} existan. Detalle: {e}") # type: ignore
    except Exception as e:
        print(f"Error al generar el JSON: {e}")



def obtener_datos_completos() -> pd.DataFrame:
    try:
        conn = sqlite3.connect(RUTA_DB / NOMBRE_DB)
        query = f"SELECT * FROM {TABLA_IMPORTACION}"

        df = pd.read_sql(query, conn, parse_dates=['date'])
        conn.close()
        return df

    except sqlite3.Error as e:
        print(f"Error al consultar la base de datos: {e}")
        return pd.DataFrame()
    
# ====================================================================
# Uso Inicial (Para probar o forzar la carga)
# ====================================================================

if __name__ == '__main__':
    # Este bloque solo se ejecuta si corres el script directamente para probar.
    cargar_datos_iniciales()
    
    df_prueba = obtener_datos_completos()
    print("\nPrimeras 5 filas del DataFrame recuperado:")
    print(df_prueba.head())
