from pathlib import Path

# =========================================================================
# 1. Definición de constantes generales
# =========================================================================
RUTA_BASE: Path = Path(__file__).resolve().parent.parent.parent.parent

CARPETA_APLICACION="dashboard_cientifico"

RUTA_PAQUETE_PRINCIPAL: Path = RUTA_BASE / CARPETA_APLICACION

RUTA_ARCHIVOS: Path = RUTA_PAQUETE_PRINCIPAL / "archivos"
CARPETA_ARCHIVOS = f"{CARPETA_APLICACION}/archivos"
RUTA_DB: Path = RUTA_PAQUETE_PRINCIPAL / "db"
RUTA_DESCARGAS: Path = RUTA_PAQUETE_PRINCIPAL / "descargas"
CARPETA_DESCARGAS = f"{CARPETA_APLICACION}/descargas"
RUTA_IMAGENES: Path = RUTA_PAQUETE_PRINCIPAL / "img"
CARPETA_IMG = f"{CARPETA_APLICACION}/img"


# =========================================================================
# 2. Definición de constantes particulares
# =========================================================================
RUTA_STREAMLIT: Path = RUTA_PAQUETE_PRINCIPAL / 'aplicacion/controlador/app_dashboard.py'

# --- CONFIGURACIÓN DB ---
NOMBRE_DB: str = "datos_covid.sqlite"

TABLA_IMPORTACION = 'datos_covid'

# --- CONFIGURACIÓN DE ARCHIVOS ---
NOMBRE_ARCHIVO_ENTRADA: str = "datos_covid.csv"
RUTA_ARCHIVO_ENTRADA: Path = RUTA_ARCHIVOS / NOMBRE_ARCHIVO_ENTRADA

NOMBRE_JSON = 'datos_covid.json'
NOMBRE_JSON_ELIMINADOS='datos_eliminados.json'

# --- DIAS DE LA SEMANA ---
DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

# --- MAPEO DE MÉTRICAS ---
# Mapeo de las métricas del proyecto a las columnas del CSV
METRICAS_MAPEO = {
    'num_def': 'deceased',
    'new_cases': 'new_cases',
    'num_hosp': 'num_hosp',
    'num_uci': 'num_uci'
}
METRICAS_CLAVES = list(METRICAS_MAPEO.keys()) 

# Opciones de menú para la selección de gráficos
OPCIONES_GRAFICOS = {
    1: {'metrica': 'num_def', 'nombre': 'Defunciones'},
    2: {'metrica': 'new_cases', 'nombre': 'Casos'},
    3: {'metrica': 'num_hosp', 'nombre': 'Hospitalizados'},
    4: {'metrica': 'num_uci', 'nombre': 'UCI'}
}
