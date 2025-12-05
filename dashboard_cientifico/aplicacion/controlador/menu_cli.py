from typing import Dict, List
import matplotlib.pyplot as plt

from dashboard_cientifico.aplicacion.modelo.carga_datos import (reset_datos, 
                                                                obtener_datos_completos)
                                                                # ... otras funciones que necesites del Modelo

from dashboard_cientifico.aplicacion.modelo.funciones_graficos import (obtener_acumulados_por_dia_semana,
                                                                       obtener_totales_por_provincia)

from dashboard_cientifico.aplicacion.vista.vista_cli import (grafico_acumulados_dia_cli,
                                                             grafico_queso_provincia_cli)

from dashboard_cientifico.aplicacion.config.settings import METRICAS_ANALISIS

plt.ion()


def obtener_metricas_para_menu() -> Dict[str, str]:
    metricas_menu = {
        str(i + 1): col_key 
        for i, col_key in enumerate(METRICAS_ANALISIS.keys())
    }
    return metricas_menu


def seleccionar_metrica() -> str:
    while True:
        print("\n--- Selección de Métrica ---")
        
        metricas_menu_keys = obtener_metricas_para_menu()
        
        for num, col_key in metricas_menu_keys.items():
            nombre_descriptivo = METRICAS_ANALISIS.get(col_key, col_key) # <-- Usa METRICAS_ANALISIS
            print(f"{num}. {nombre_descriptivo}")

        opcion = input("Seleccione el número de la métrica: ") # <-- ¡AQUÍ ESTÁ!
        
        # 3. Validar la opción
        if opcion in metricas_menu_keys:
            return metricas_menu_keys[opcion] # Devuelve el nombre de la columna ('num_def', etc.)
        else:
            print("Opción no válida. Intente de nuevo.")

            
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
        if opcion == '1' or opcion == '2':
            # --------------------------------------------------------
            # AÑADIDO: LÓGICA DE SELECCIÓN DE PARÁMETROS
            # --------------------------------------------------------
            
            # 1. Seleccionar la métrica a analizar
            metrica_columna = seleccionar_metrica() # <-- ¡AQUÍ ESTÁ LA LLAMADA!
            
            # 3. Obtener el título descriptivo
            # Buscamos el valor descriptivo (ej: 'Defunciones') a partir de la columna ('num_def')
            titulo_metrica = METRICAS_ANALISIS.get(metrica_columna, metrica_columna)
            
            # --------------------------------------------------------
            # EJECUCIÓN DEL GRÁFICO
            # --------------------------------------------------------

        if opcion == '1':
            print("Preparando datos y mostrando Gráfico Acumulado Diario...")
 
            df_acumulado = obtener_acumulados_por_dia_semana(df_completo, metrica="num_def", cargas_a_filtrar=['202105'])

            grafico_acumulados_dia_cli(titulo_metrica, df_acumulado, "num_def")
            
        elif opcion == '2':
            print("Preparando datos y mostrando Gráfico Tarta por Provincia...")

            df_provincia = obtener_totales_por_provincia(df_completo, metrica="new_cases", cargas_a_filtrar=['202105'])
            
            grafico_queso_provincia_cli(titulo_metrica, df_provincia, "new_cases") 
            
        elif opcion == '0':
            print("Saliendo de la aplicación. ¡Hasta pronto!")
            break
            
        else:
            print("Opción no válida. Por favor, introduzca un número del menú.")

if __name__ == '__main__':

    controlador_cli()