"""
Ejecución: python -m dashboard_cientifico.aplicacion.main

"""
from pathlib import Path
import subprocess
import os

RUTA_PAQUETE = Path(__file__).resolve().parent.parent
RUTA_PROYECTO_FINAL = RUTA_PAQUETE.parent
env = os.environ.copy()
env['PYTHONPATH'] = str(RUTA_PROYECTO_FINAL)

from dashboard_cientifico.aplicacion.config.settings import RUTA_STREAMLIT


def iniciar_dashboard_streamlit():
    if not os.path.exists(RUTA_STREAMLIT):
        print(f"Error: No se encontró el script de Streamlit en: {RUTA_STREAMLIT}")
        return

    print("\nIniciando Streamlit Dashboard...")

    try:
        subprocess.run(["streamlit", "run", RUTA_STREAMLIT], check=True, env=env)
        
    except FileNotFoundError:
        print("\nError: El comando 'streamlit' no se encontró.")
        print("Asegúrate de que estás en el entorno virtual de Poetry o que Streamlit está instalado correctamente.")
        
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar Streamlit: {e}")

if __name__ == "__main__":
    iniciar_dashboard_streamlit()

