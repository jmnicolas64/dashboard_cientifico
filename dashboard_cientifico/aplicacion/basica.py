"""
Ejecución: python -m dashboard_cientifico.aplicacion.basica

"""

from .controlador import menu_cli

def main():
    try:
        menu_cli.controlador_cli()      
    except Exception as e:
        print(f"Ocurrió un error inesperado al ejecutar la aplicación CLI: {e}")

if __name__ == '__main__':
    main()