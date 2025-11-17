# C:\...\dashboard_cientifico\main.py

import subprocess
import os

# Define la ruta al script principal de Streamlit (la nueva VISTA principal)
# Asumiendo que has creado app_dashboard.py dentro de la carpeta controlador
STREAMLIT_SCRIPT_PATH = 'controlador/app_dashboard.py' 

def iniciar_dashboard_streamlit():
    """Lanza la aplicación de Streamlit."""
    # Necesitas la ruta completa para ejecutarlo desde la raíz
    script_path = os.path.join(os.path.dirname(__file__), STREAMLIT_SCRIPT_PATH)
    
    if not os.path.exists(script_path):
        print(f"❌ Error: No se encontró el script de Streamlit en: {script_path}")
        return

    print("🚀 Iniciando Streamlit Dashboard...")
    
    # Comando para iniciar Streamlit
    # El subprocess se usa para ejecutar un comando externo
    try:
        subprocess.run(["streamlit", "run", script_path], check=True)
    except FileNotFoundError:
        print("\n❌ Error: El comando 'streamlit' no se encontró.")
        print("Asegúrate de que estás en el entorno virtual de Poetry o que Streamlit está instalado correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al ejecutar Streamlit: {e}")

if __name__ == "__main__":
    iniciar_dashboard_streamlit()