"""
Ejecución: python -m dashboard_cientifico.aplicacion.main
"""

from ..aplicacion.controlador.controlador import iniciar_version_basica


def menu_selector_version():
    """Permite al usuario elegir la versión a ejecutar (Consola o Web)."""
    while True:
        print("\n" + "#"*60)
        print("         💻 PROYECTO FINAL 3: DASHBOARD CIENTÍFICO")
        print("             (Selección de Versión)")
        print("#"*60)
        print("1. Versión Básica (Consola, JSON)")
        print("2. Versión Ampliada (Web, Django/BBDD)")
        print("3. Salir")
        print("="*60)
        
        opcion = input("Selecciona la versión (1-3): ")
        
        if opcion == '1':
            # Llamada al controlador de la versión básica
            iniciar_version_basica() 
        elif opcion == '2':
            # ¡Aquí irá la lógica de Django!
            # ampliado.iniciar_version_ampliada() 
            print("Versión Ampliada aún en desarrollo. ¡Volviendo al menú principal!")
        elif opcion == '3':
            print("Programa finalizado. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    # La aplicación arranca aquí
    menu_selector_version()