import pandas as pd
from typing import Dict, List

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

# dashboard_cientifico/aplicacion/modelo/analisis_service.py

def obtener_datos_agrupados(df: pd.DataFrame, columna_agrupacion: str) -> pd.DataFrame:
    """
    Función de servicio para agrupar y calcular estadísticas (ej. media, suma).
    """
    # Lógica de Pandas pura:
    df_agrupado = df.groupby(columna_agrupacion)['columna_numerica'].agg(['sum', 'mean']).reset_index()
    return df_agrupado


def obtener_datos_filtrados(df: pd.DataFrame, columna: str, valor: str) -> pd.DataFrame:
    """
    Función de servicio para aplicar un filtro simple a los datos.
    """
    # Lógica de Pandas pura:
    df_filtrado = df[df[columna] == valor].copy()
    return df_filtrado

# Aquí irían todas las funciones que manipulen datos con Pandas (Model)

# dashboard_cientifico/aplicacion/modelo/datos_service.py


def preparar_datos_csv(df: pd.DataFrame) -> str:
    """
    Prepara el DataFrame para su descarga, convirtiéndolo a una cadena CSV.
    """
    # Lógica de Pandas pura: to_csv es la forma más limpia de hacer esto
    return df.to_csv(index=False, sep=';').encode('utf-8') # type: ignore


# dashboard_cientifico/aplicacion/modelo/funciones_graficos.py (Añadir estas funciones)
# Definición de la ordenación para los días de la semana
DAY_ORDER_ES = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

# --------------------------------------------------------------------------
# Lógica para Ejercicio 2 (Agrupación por Día)
# --------------------------------------------------------------------------

def obtener_acumulados_por_dia_semana(df: pd.DataFrame, metrica: str) -> pd.DataFrame:
    """
    [PURA - Modelo] Agrupa los datos por día de la semana y calcula el total acumulado 
    para la métrica seleccionada (Ejercicio 2).
    """
    if 'date' not in df.columns:
        raise ValueError("Columna 'date' no encontrada. Asegúrate de la pre-carga.")
        
    # Calcular el día de la semana (asumiendo que df['date'] es datetime)
    df['day_of_week'] = df['date'].dt.day_name(locale='es_ES.utf8') # Usa el locale español

    # Agrupar y sumar
    df_dia = df.groupby('day_of_week')[metrica].sum().reset_index()
    
    # Asegurar el orden de los días de la semana
    df_dia['day_of_week'] = pd.Categorical(df_dia['day_of_week'], categories=DAY_ORDER_ES, ordered=True)
    df_dia = df_dia.sort_values('day_of_week')
    
    return df_dia

# --------------------------------------------------------------------------
# Lógica para Ejercicio 3 (Agrupación por Provincia y Máx/Mín)
# --------------------------------------------------------------------------

def obtener_totales_por_provincia(df: pd.DataFrame, metrica: str) -> pd.DataFrame:
    """
    [PURA - Modelo] Agrupa los datos por provincia y calcula el total acumulado para la métrica.
    """
    if 'province' not in df.columns:
        raise ValueError("Columna 'province' no encontrada.")
        
    df_provincia_total = df.groupby('province')[metrica].sum().reset_index()
    return df_provincia_total


def obtener_max_min_provincia(df_provincia_total: pd.DataFrame, metrica: str) -> Dict:
    """
    [PURA - Modelo] Calcula la provincia con el máximo y mínimo valor de la métrica.
    """
    max_row = df_provincia_total.loc[df_provincia_total[metrica].idxmax()]
    min_row = df_provincia_total.loc[df_provincia_total[metrica].idxmin()]
    
    return {
        'max_provincia': max_row['province'],
        'max_valor': max_row[metrica],
        'min_provincia': min_row['province'],
        'min_valor': min_row[metrica]
    }
