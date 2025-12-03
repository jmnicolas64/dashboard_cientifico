import json
from pathlib import Path
import pandas as pd
from typing import Dict, Union, Any, Tuple, List
from dashboard_cientifico.aplicacion.config.settings import (RUTA_DESCARGAS,
                                                             NOMBRE_CSV_DESCARGAS,
                                                             RUTA_ARCHIVOS,
                                                             NOMBRE_GEOJSON)


ORDEN_DIAS = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
ResultType = Tuple[Union[Dict[str, Any], None], Union[str, None]]

def obtener_evolucion_nacional(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepara los datos para la evolución temporal nacional.
    """
    # Lógica de Pandas pura (groupby, sum, reset_index)
    df_nacional = df.groupby('date')[['daily_cases', 'daily_cases_avg7']].sum().reset_index()
    return df_nacional


def obtener_ia14_por_ccaa(df: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    """
    Prepara los datos para la distribución geográfica de IA14.
    """
    # 1. Encontrar el último día
    ultimo_dia = df['date'].max()
    df_ultimo_dia = df[df['date'] == ultimo_dia]
    
    # 2. Agregación Geográfica
    df_ccaa = df_ultimo_dia.groupby('ccaa').agg(
        ia14_max=('ia14', 'max')
    ).reset_index()

    # 3. Ordenar
    df_ccaa = df_ccaa.sort_values(by='ia14_max', ascending=False)
    
    return df_ccaa, ultimo_dia.strftime('%Y-%m-%d')


def obtener_datos_agrupados(df: pd.DataFrame, columna_agrupacion: str) -> pd.DataFrame:
    """
    Función de servicio para agrupar y calcular estadísticas (ej. media, suma).
    """
    # Lógica de Pandas pura:
    df_agrupado = df.groupby(columna_agrupacion)['columna_numerica'].agg(['sum', 'mean']).reset_index()
    return df_agrupado


def obtener_datos_filtrados(df: pd.DataFrame, columna: str, valor: str, columnas_ordenadas: list) -> pd.DataFrame:
    df_filtrado = df[df[columna] == valor].copy()
    columnas_existentes = [col for col in columnas_ordenadas if col in df_filtrado.columns]
    df_filtrado = df_filtrado[columnas_existentes]

    return df_filtrado


def obtener_acumulados_por_dia_semana(df: pd.DataFrame, metrica: str, cargas_a_filtrar: list) -> pd.DataFrame:
    if 'date' not in df.columns:
        raise ValueError("Columna 'date' no encontrada. Asegúrate de la pre-carga.")

    df['dia_semana'] = df['date'].dt.day_name(locale='es_ES.utf8') # type: ignore

    df_dia = (
        df[df['carga_id'].isin(cargas_a_filtrar)]
              .groupby('dia_semana')[metrica]
              .sum()
              .reset_index()
              )

    df_dia['dia_semana'] = pd.Categorical(df_dia['dia_semana'], categories=ORDEN_DIAS, ordered=True)
    df_dia = df_dia.sort_values('dia_semana')
    
    return df_dia


def obtener_totales_por_provincia(df: pd.DataFrame, metrica: str, cargas_a_filtrar: list) -> pd.DataFrame:
    if 'province' not in df.columns:
        raise ValueError("Columna 'province' no encontrada.")
        
    df_provincia_total = (
        df[df['carga_id'].isin(cargas_a_filtrar)]
        .groupby('province')[metrica]
        .sum()
        .reset_index()
        )
    
    total_metrica = df_provincia_total[metrica].sum()

    df_provincia_total['porcentaje'] = (
        df_provincia_total[metrica] / total_metrica
    ) * 100
    
    return df_provincia_total


def obtener_max_min_provincia(df_provincia_total: pd.DataFrame, metrica: str) -> Dict:
    if df_provincia_total.empty:
        return {
            'max_provincia': 'N/D',
            'max_valor': 0,
            'min_provincia': 'N/D',
            'min_valor': 0
        }
    
    max_row = df_provincia_total.loc[df_provincia_total[metrica].idxmax()]
    min_row = df_provincia_total.loc[df_provincia_total[metrica].idxmin()]
    
    return {
        'max_provincia': max_row['province'],
        'max_valor': max_row[metrica],
        'min_provincia': min_row['province'],
        'min_valor': min_row[metrica]
    }


def cargar_json(ruta: Path) -> ResultType:   
    if not ruta.is_file():
        error = f"Archivo no encontrado: {ruta.name}"
        return None, error

    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido_json = f.read()
            
        datos_json = json.loads(contenido_json)
        return datos_json, None
        
    except json.JSONDecodeError:
        error = "Error de formato JSON: El archivo contiene datos inválidos."
        return None, error
        
    except Exception as e:
        error = f"Error al leer el archivo: {e}"
        return None, error


def preparar_datos_csv(df: pd.DataFrame) -> str:
    return df.to_csv(index=False, sep=';').encode('utf-8') # type: ignore


def guardar_datos_csv(df: pd.DataFrame):
    RUTA_DESCARGAS.mkdir(parents=True, exist_ok=True)

    ruta_completa = RUTA_DESCARGAS / NOMBRE_CSV_DESCARGAS
    
    df.to_csv(ruta_completa, index=False, encoding='utf-8')
    
    return ruta_completa


def obtener_evolucion_mensual(df: pd.DataFrame, metrica: str) -> pd.DataFrame:
    if not pd.api.types.is_datetime64_any_dtype(df['date']):
        df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
        
    df_evolucion = (
        df.groupby(df['date'].dt.to_period('M'))[metrica] # type: ignore
        .sum()
        .reset_index()
    ) 
    
    df_evolucion['date'] = df_evolucion['date'].dt.to_timestamp()
    
    return df_evolucion


def obtener_matriz_correlacion_mensual(df: pd.DataFrame, metricas: list) -> pd.DataFrame:
    """
    Agrupa el DF por mes y calcula la matriz de correlación de Pearson entre las métricas.
    """
    # 1. Agrupar por mes y sumar todas las métricas relevantes
    df_mensual = (
        df.groupby(df['date'].dt.to_period('M'))[metricas] # type: ignore
        .sum()
    )
    
    # 2. Calcular la matriz de correlación
    matriz_corr = df_mensual.corr(method='pearson')
    
    return matriz_corr


def cargar_geojson() -> dict:
    ruta: Path = RUTA_ARCHIVOS / NOMBRE_GEOJSON
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: No se encontró el archivo GeoJSON en la ruta {ruta}. Asegúrate de que esté en el directorio correcto.")

def obtener_datos_geograficos(df: pd.DataFrame, metrica: str) -> pd.DataFrame:
    """
    [MODELO] Agrega los datos por Comunidad Autónoma (CCAA) para el análisis geográfico,
    sumando el total de la métrica en todo el período filtrado.
    """
    # Se asume que la columna de CCAA se llama 'ccaa'
    if 'ccaa' not in df.columns:
        raise ValueError("El DataFrame no contiene la columna 'ccaa' necesaria para el análisis geográfico.")
        
    # Agregación Geográfica: Sumar la métrica seleccionada por CCAA
    df_ccaa = df.groupby('ccaa')[metrica].sum().reset_index()
    df_ccaa.rename(columns={metrica: 'Total_Metrica'}, inplace=True)
    return df_ccaa

