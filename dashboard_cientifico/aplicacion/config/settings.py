# dashboard_cientifico/aplicacion/config/settings.py

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

# Nota: Usamos la RUTA_BASE para construir rutas absolutas.

# La carpeta que contiene el código de la aplicación (dashboard_cientifico/)
RUTA_PAQUETE_PRINCIPAL: Path = RUTA_BASE / "dashboard_cientifico"

# Rutas a tus carpetas de recursos (datos, db, descargas)
RUTA_ARCHIVOS: Path = RUTA_PAQUETE_PRINCIPAL / "archivos"
CARPETA_ARCHIVOS = "dashboard_cientifico/archivos"
RUTA_DB: Path = RUTA_PAQUETE_PRINCIPAL / "db"
RUTA_DESCARGAS: Path = RUTA_PAQUETE_PRINCIPAL / "descargas"
CARPETA_DESCARGAS = "dashboard_cientifico/descargas"
RUTA_IMAGENES: Path = RUTA_PAQUETE_PRINCIPAL / "img"
CARPETA_IMG = "dashboard_cientifico/img"


# =========================================================================
# 3. Definición de CONSTANTES (Base de Datos y Archivos de Entrada)
# =========================================================================

# Nombre del archivo de la base de datos que se guardará en la carpeta 'db'
NOMBRE_DB: str = "datos_analisis.sqlite"

# Ruta ABSOLUTA completa a la base de datos (para usar con librerías como SQLAlchemy)
RUTA_SQLITE_DB: Path = RUTA_DB / NOMBRE_DB

# Nombre del archivo CSV de entrada (ejemplo)
NOMBRE_ARCHIVO_ENTRADA: str = "datos_mediciones.csv"

# Ruta ABSOLUTA completa al archivo de entrada (asumiendo que está en la carpeta 'archivos')
RUTA_ARCHIVO_ENTRADA: Path = RUTA_ARCHIVOS / NOMBRE_ARCHIVO_ENTRADA
