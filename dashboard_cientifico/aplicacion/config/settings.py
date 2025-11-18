from pathlib import Path

# =========================================================================
# 1. Definición de la RUTA BASE del proyecto
# =========================================================================

# Path(__file__).resolve() obtiene la ruta absoluta de este archivo (settings.py).
# .parent.parent.parent.parent sube 4 niveles para llegar a la raíz del repositorio.
# La ruta base es C:\...\Proyecto_Final\
RUTA_BASE: Path = Path(__file__).resolve().parent.parent.parent.parent

# =========================================================================
# 2. Definición de RUTAS de Recursos
# =========================================================================

CARPETA_CODIGO="dashboard_cientifico"

RUTA_PAQUETE_PRINCIPAL: Path = RUTA_BASE / CARPETA_CODIGO
RUTA_STREAMLIT: Path = RUTA_PAQUETE_PRINCIPAL / 'aplicacion/controlador/app_dashboard.py'

# Rutas a tus carpetas de recursos (datos, db, descargas)
RUTA_ARCHIVOS: Path = RUTA_PAQUETE_PRINCIPAL / "archivos"
CARPETA_ARCHIVOS = f"{CARPETA_CODIGO}/archivos"
RUTA_DB: Path = RUTA_PAQUETE_PRINCIPAL / "db"
RUTA_DESCARGAS: Path = RUTA_PAQUETE_PRINCIPAL / "descargas"
CARPETA_DESCARGAS = f"{CARPETA_CODIGO}/descargas"
RUTA_IMAGENES: Path = RUTA_PAQUETE_PRINCIPAL / "img"
CARPETA_IMG = f"{CARPETA_CODIGO}/img"


# =========================================================================
# 3. Definición de CONSTANTES (Base de Datos y Archivos de Entrada)
# =========================================================================

# Nombre del archivo de la base de datos que se guardará en la carpeta 'db'
NOMBRE_DB: str = "datos_analisis.sqlite"

# Ruta ABSOLUTA completa a la base de datos (para usar con librerías como SQLAlchemy)
RUTA_SQLITE_DB: Path = RUTA_DB / NOMBRE_DB

# Nombre del archivo CSV de entrada (ejemplo)
NOMBRE_ARCHIVO_ENTRADA: str = "datos_covid.csv"

# Ruta ABSOLUTA completa al archivo de entrada (asumiendo que está en la carpeta 'archivos')
RUTA_ARCHIVO_ENTRADA: Path = RUTA_ARCHIVOS / NOMBRE_ARCHIVO_ENTRADA

# --- CONFIGURACIÓN DE ARCHIVOS ---
NOMBRE_JSON = 'datos_covid.json'

# --- MÉTODOS DE AGRUPACIÓN ---
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
