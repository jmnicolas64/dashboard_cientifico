# Inicio.py (Función modificada para el dominio de Pandas)

# ... (otras funciones y variables) ...

def _inicializar_dataframe():
    """
    Obtiene el DataFrame base de la DB y aplica las transformaciones
    esenciales de Pandas (Series Temporales y Métricas Derivadas)
    para el análisis en el Dashboard.
    """
    # 1. Obtener el DataFrame base de la DB
    df = obtener_datos_completos() 
    
    if df.empty:
        # Asignar un DataFrame vacío y salir si no hay datos.
        st.session_state[CLAVE_DATAFRAME] = pd.DataFrame() 
        return

    # 2. ASEGURAR SERIES TEMPORALES Y AGRUPACIÓN
    
    # [Dominio Pandas 1]: Convertir la columna de fecha a formato datetime
    # Esto es CRÍTICO para cualquier análisis temporal.
    df['date'] = pd.to_datetime(df['date'])
    
    # 3. GENERACIÓN DE MÉTRICAS CLAVE
    
    # La clave para estos cálculos es usar .groupby('province') antes del cálculo
    # para asegurar que las operaciones (rolling, diff) se realicen por separado en cada provincia,
    # sin mezclar los datos geográficos.
    
    # [Dominio Pandas 2]: Cálculo de la Media Móvil de 7 días (rolling().mean())
    # Transforma la columna 'daily_cases' aplicando la media móvil, agrupando por provincia.
    df['daily_cases_avg7'] = df.groupby('province')['daily_cases'].transform(
        lambda x: x.rolling(window=7, min_periods=1).mean()
    )
    
    # [Dominio Pandas 3]: Cálculo de Nuevos Casos Diarios (diff()) a partir de acumulados.
    # Asumimos que la columna 'deceased' es acumulada. Calculamos los fallecidos diarios.
    # El fillna(0) asegura que el primer día (donde diff() devuelve NaN) sea 0.
    df['daily_deaths_calculated'] = df.groupby('province')['deceased'].diff().fillna(0)
    
    # Calculamos la media móvil para los fallecidos diarios calculados
    df['daily_deaths_avg7'] = df.groupby('province')['daily_deaths_calculated'].transform(
        lambda x: x.rolling(window=7, min_periods=1).mean()
    )
    
    # [Dominio Pandas 4]: Cálculo de Tasas (Arithmetic + Transform)
    # Calculamos los casos acumulados por 100,000 habitantes.
    # Se usa la columna 'poblacion' para normalizar los datos y hacer comparaciones justas.
    df['cases_per_100k'] = (df['cases_accumulated'] / df['poblacion']) * 100000

    # 4. ASIGNAR EL DATAFRAME TRANSFORMADO
    st.session_state[CLAVE_DATAFRAME] = df

# ... (Resto del script Inicio.py)