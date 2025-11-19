"""
Ejecución: python -m dashboard_cientifico.aplicacion.main

Base de Datos es la Fuente de Verdad. Se genera json para exportacion de datos
"""

import subprocess
import os
from dashboard_cientifico.aplicacion.config.settings import RUTA_STREAMLIT


def iniciar_dashboard_streamlit():
    if not os.path.exists(RUTA_STREAMLIT):
        print(f"❌ Error: No se encontró el script de Streamlit en: {RUTA_STREAMLIT}")
        return

    print("🚀 Iniciando Streamlit Dashboard...")

    try:
        subprocess.run(["streamlit", "run", RUTA_STREAMLIT], check=True)
        
    except FileNotFoundError:
        print("\n❌ Error: El comando 'streamlit' no se encontró.")
        print("Asegúrate de que estás en el entorno virtual de Poetry o que Streamlit está instalado correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al ejecutar Streamlit: {e}")

if __name__ == "__main__":
    iniciar_dashboard_streamlit()