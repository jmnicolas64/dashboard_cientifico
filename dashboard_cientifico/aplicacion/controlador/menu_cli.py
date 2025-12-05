from dashboard_cientifico.aplicacion.modelo.carga_datos import (reset_datos, 
                                                                obtener_datos_completos)
                                                                # ... otras funciones que necesites del Modelo

from dashboard_cientifico.aplicacion.modelo.funciones_graficos import (obtener_acumulados_por_dia_semana,
                                                                       obtener_totales_por_provincia)

from dashboard_cientifico.aplicacion.vista import vista_cli

def mostrar_menu():
    """Muestra el menú de opciones al usuario y pide una entrada."""
    print("\n" + "="*40)
    print("      Dashboard Científico (Versión CLI)")
    print("="*40)
    print("1. Mostrar Gráfico Acumulado Diario (Matplotlib)")
    print("2. Mostrar Gráfico Tarta por Provincia (Matplotlib)")
    print("0. Salir")
    print("="*40)
    
    opcion = input("Seleccione una opción: ")
    return opcion


def controlador_cli():
    """
    Función principal del controlador CLI que gestiona el flujo del menú.
    """
    print("Iniciando aplicación CLI...")
    
    #try:
        #reset_datos()
        #print("Base de datos cargada e inicializada correctamente.")
    #except Exception as e:
        #print(f"ERROR: No se pudo inicializar la base de datos: {e}")
        #return # Termina si la inicialización falla

    df_completo = obtener_datos_completos()
    if df_completo.empty:
        print("ERROR: No se pudieron cargar los datos de la base de datos.")
        # Manejo de error...
        # ...

    while True:
        opcion = mostrar_menu()
        
        if opcion == '1':
            print("Preparando datos y mostrando Gráfico Acumulado Diario...")
            # 1. Llamar al Modelo para obtener los datos
            df_acumulado = obtener_acumulados_por_dia_semana(df_completo, metrica="num_def", cargas_a_filtrar=['1', '2', '3']) # Necesitas definir qué cargas filtrar
            
            # 2. Llamar a la Vista CLI para dibujar el gráfico
            vista_cli.grafica_acumulados_dia_cli("Casos", df_acumulado, "casos_acumulados")
            
        elif opcion == '2':
            print("Preparando datos y mostrando Gráfico Tarta por Provincia...")
            # 1. Llamar al Modelo para obtener los datos
            df_provincia = obtener_totales_por_provincia(df_completo, metrica="new_cases", cargas_a_filtrar=['1', '2', '3'])
            
            # 2. Llamar a la Vista CLI para dibujar el gráfico
            # El controlador se encarga de llamar a la función del Modelo que calcula max/min
            # ... y pasarlos a la vista si es necesario
            vista_cli.grafica_queso_provincia_cli("Hospitalizados", df_provincia, "Hospitalizados_total") 
            
        elif opcion == '0':
            print("Saliendo de la aplicación. ¡Hasta pronto!")
            break
            
        else:
            print("Opción no válida. Por favor, introduzca un número del menú.")

if __name__ == '__main__':

    controlador_cli()