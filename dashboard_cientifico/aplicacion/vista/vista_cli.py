# dashboard_cientifico/aplicacion/vistas/vista_cli.py
import matplotlib
matplotlib.use('TkAgg')
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict
from dashboard_cientifico.aplicacion.modelo.funciones_graficos import obtener_max_min_provincia
from dashboard_cientifico.aplicacion.config.settings import (RUTA_ARCHIVOS,
                                                             NOMBRE_COMENTARIOS)

plt.style.use('seaborn-v0_8-whitegrid')

def mostrar_mensaje_resumen(titulo: str, max_min_data: Dict):
    print("\n" + "-"*50)
    print(f"       Resultados del Análisis de {titulo}\n")
    #print("="*50)
    print(f"Provincia con valor MÁXIMO: {max_min_data['max_provincia']} (Total: {max_min_data['max_valor']:,})")
    print(f"Provincia con valor MÍNIMO: {max_min_data['min_provincia']} (Total: {max_min_data['min_valor']:,})")
    #print("="*50 + "\n")


def grafico_acumulados_dia_cli(titulo: str, df_dia: pd.DataFrame, metrica: str):
    if df_dia.empty:
        print(f"AVISO: No hay datos para mostrar el gráfico de {titulo}.")
        return

    plt.figure(figsize=(10, 6))
    
    sns.barplot(
        x='dia_semana', 
        y=metrica, 
        data=df_dia, 
        palette='viridis',
        hue='dia_semana',
        legend=False,
        hue_order=df_dia['dia_semana'].tolist()
    )
    
    plt.title(f"Total Acumulado de {titulo} por Día de la Semana", fontsize=16)
    plt.xlabel('Día de la Semana', fontsize=12)
    plt.ylabel(f'Total Acumulado ({titulo})', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.show()


def grafico_queso_provincia_cli(titulo: str, df_provincia_total: pd.DataFrame, metrica: str):
    if df_provincia_total.empty:
        print(f"AVISO: No hay datos para mostrar el gráfico de {titulo}.")
        return


    max_min_data = obtener_max_min_provincia(df_provincia_total, metrica)
    mostrar_mensaje_resumen(titulo, max_min_data)

    plt.figure(figsize=(10, 10))

    valores = df_provincia_total[metrica]
    etiquetas = df_provincia_total['province']

    plt.pie(
        valores, 
        labels=etiquetas, # type: ignore
        autopct='%1.1f%%', # Formato para mostrar el porcentaje en la tarta
        startangle=90,
        wedgeprops={'edgecolor': 'black', 'linewidth': 0.7}
    )

    plt.title(f"Distribución Total de {titulo} por Provincia", fontsize=16)
    plt.axis('equal') # Asegura que el gráfico es un círculo

    plt.show()


def mostrar_archivo_md_cli() -> str:
    ruta_archivo=RUTA_ARCHIVOS / NOMBRE_COMENTARIOS
    try:
        if not ruta_archivo.exists():
            print(f"ERROR: Archivo no encontrado en: {ruta_archivo}")
            input("\nPresione ENTER para volver al menú...")
            return ""

        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()

        return(contenido)

    except Exception as e:
        return(f"ERROR al leer el archivo Markdown: {e}")