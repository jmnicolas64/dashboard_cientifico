from pathlib import Path

# =========================================================================
# 1. Definición de constantes generales (cambiar sólo la variable indicada)
# =========================================================================

RUTA_PAQUETE_PRINCIPAL: Path = Path(__file__).resolve().parent.parent.parent

CARPETA_APLICACION="dashboard_cientifico" # En esta sección 1 sólo hay que cambiar este parámetro.

RUTA_ARCHIVOS: Path = RUTA_PAQUETE_PRINCIPAL / "archivos"
CARPETA_ARCHIVOS = f"{CARPETA_APLICACION}/archivos"
RUTA_DB: Path = RUTA_PAQUETE_PRINCIPAL / "db"
CARPETA_DB = f"{CARPETA_APLICACION}/db"
RUTA_DESCARGAS: Path = RUTA_PAQUETE_PRINCIPAL / "descargas"
CARPETA_DESCARGAS = f"{CARPETA_APLICACION}/descargas"
RUTA_IMAGENES: Path = RUTA_PAQUETE_PRINCIPAL / "img"
CARPETA_IMG = f"{CARPETA_APLICACION}/img"

# =========================================================================
# 2. Definición de constantes particulares (cambiar todas las variables)
# =========================================================================

RUTA_STREAMLIT: Path = RUTA_PAQUETE_PRINCIPAL / 'aplicacion/Inicio.py'
CLAVE_DATAFRAME = 'datos_principales'

# --- CONFIGURACIÓN DB ---
NOMBRE_DB: str = "datos_covid.sqlite"
TABLA_DATOS_COVID = 'datos_covid'
TABLA_CARGAS_ID = 'cargas_id'

# --- CONFIGURACIÓN DE ARCHIVOS ---
NOMBRE_ARCHIVO_ENTRADA: str = "datos_covid05_original.csv"
RUTA_ARCHIVO_ENTRADA: Path = RUTA_ARCHIVOS / NOMBRE_ARCHIVO_ENTRADA
CARGA_ID_INICIAL='202105'
CARPETA_CARGADOS='cargados'


RUTA_COPIA_ARCHIVOS = RUTA_PAQUETE_PRINCIPAL / "repositorio_archivos"

NOMBRE_JSON_PEDIDO = 'datos_covid.json'
NOMBRE_JSON_ELIMINADOS='datos_eliminados.json'
NOMBRE_JSON_CARGAS_ID='carga_ids.json'

NOMBRE_CSV_DESCARGAS='datos_exportados.csv'
NOMBRE_GEOJSON = 'comunidades_autonomas.geojson'
NOMBRE_COMENTARIOS='proyecto_final.md'

METRICAS_ANALISIS = {
    "num_def": "Defunciones",
    "new_cases": "Casos",
    "num_hosp": "Hospitalizados",
    "num_uci": "UCI"
}