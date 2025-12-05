import sys
from typing import Dict
import matplotlib.pyplot as plt

from dashboard_cientifico.aplicacion.modelo.carga_datos import (reset_datos, 
                                                                obtener_datos_completos,
                                                                verificar_db,
                                                                crear_tabla_carga_ids,
                                                                cargar_datos,
                                                                generar_json,
                                                                )
                                                                

from dashboard_cientifico.aplicacion.modelo.funciones_graficos import (obtener_acumulados_por_dia_semana,
                                                                       obtener_totales_por_provincia)

from dashboard_cientifico.aplicacion.vista.vista_cli import (grafico_acumulados_dia_cli,
                                                             grafico_queso_provincia_cli,
                                                             mostrar_archivo_md_cli)

from dashboard_cientifico.aplicacion.vista.vista_menu import (TEXTO_OPCIONES,
                                                              mostrar_menu,
                                                              mostrar_despedida,
                                                              solicitar_opcion,
                                                              mostrar_mensaje)

from dashboard_cientifico.aplicacion.config.settings import (METRICAS_ANALISIS,
                                                             RUTA_ARCHIVO_ENTRADA,
                                                             CARGA_ID_INICIAL)

from dashboard_cientifico.aplicacion.modelo.utiles import (limpiar_pantalla,
                                                           cabecera,
                                                           pie)

CARGA_ID_UNICA='202105'
plt.ion()


def obtener_metricas_para_menu() -> Dict[str, str]:
    metricas_menu = {
        str(i + 1): col_key 
        for i, col_key in enumerate(METRICAS_ANALISIS.keys())
    }
    return metricas_menu


def seleccionar_metrica(opcion: str, titulo: str) -> str:
    while True:
        limpiar_pantalla()
        cabecera(opcion,titulo)

        print("--- Selección de Métrica ---\n")
        
        metricas_menu_keys = obtener_metricas_para_menu()
        
        for num, col_key in metricas_menu_keys.items():
            nombre_descriptivo = METRICAS_ANALISIS.get(col_key, col_key)
            print(f"{num}. {nombre_descriptivo}")

        print("0. Volver")
        opcion = input("\nSeleccione el número de la métrica: ")

        if opcion in metricas_menu_keys:
            return metricas_menu_keys[opcion]
        elif opcion=='0':
            return '0'

            
def controlador_cli():

    estado: dict = verificar_db()

    if not estado['final']:
        reset_datos()
        crear_tabla_carga_ids()      
        cargar_datos(RUTA_ARCHIVO_ENTRADA, CARGA_ID_INICIAL,"")
        generar_json()
        
        mensaje: str=(f"Datos inicializados\n"
                        f"El archivo JSON está disponible en la carpeta 'descargas'")
        
        limpiar_pantalla()
        mostrar_mensaje(mensaje)
        pie()

    df_completo = obtener_datos_completos()
    if df_completo.empty:
        print("ERROR CRITICO: No se pudieron cargar los datos de la base de datos.")
        sys.exit

    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion_principal = solicitar_opcion()

        if opcion_principal == '1' or opcion_principal == '2':
            while True:
                metrica_columna = seleccionar_metrica(opcion_principal,TEXTO_OPCIONES[int(opcion_principal)-1])
            
                if metrica_columna=='0':
                    break
            
                titulo_metrica = METRICAS_ANALISIS.get(metrica_columna, metrica_columna)

                if opcion_principal == '1':      
                    df_acumulado = obtener_acumulados_por_dia_semana(df_completo,
                                                                    metrica=metrica_columna,
                                                                    cargas_a_filtrar=[CARGA_ID_UNICA])

                    grafico_acumulados_dia_cli(titulo_metrica, df_acumulado, metrica=metrica_columna)

                elif opcion_principal == '2':
                    df_provincia = obtener_totales_por_provincia(df_completo,
                                                                metrica=metrica_columna,
                                                                cargas_a_filtrar=[CARGA_ID_UNICA])
                    
                    grafico_queso_provincia_cli(titulo_metrica, df_provincia, metrica=metrica_columna) 
                    pie()
        elif opcion_principal=='3':
            mensaje=mostrar_archivo_md_cli()
            limpiar_pantalla()
            mostrar_mensaje(mensaje)
            pie()

        elif opcion_principal == '0':
            limpiar_pantalla()
            mostrar_despedida()
            break


if __name__ == '__main__':
    controlador_cli()