# dashboard_cientifico/aplicacion/basica.py

"""
Punto de entrada principal para la versión CLI (Básica) del dashboard.
Llama a la función principal del controlador CLI.
"""

def main():
    """
    Función que inicia la aplicación CLI.
    """
    try:
        # Importamos el controlador principal de la versión CLI
        from .controlador import menu_cli
        
        # Ejecutamos la función controladora que contiene el bucle while True
        menu_cli.controlador_cli()
        
    except Exception as e:
        print(f"Ocurrió un error inesperado al ejecutar la aplicación CLI: {e}")

if __name__ == '__main__':
    main()