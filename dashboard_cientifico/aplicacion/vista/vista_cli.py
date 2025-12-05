# dashboard_cientifico/aplicacion/vistas/vista_cli.py
import matplotlib
matplotlib.use('TkAgg')
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict

from dashboard_cientifico.aplicacion.modelo.funciones_graficos import obtener_max_min_provincia

plt.style.use('seaborn-v0_8-whitegrid') # Un estilo de cuadrícula limpio

def mostrar_mensaje_resumen(titulo: str, max_min_data: Dict):
    """Muestra el resumen de maximos y mínimos en la terminal."""
    print("\n" + "="*50)
    print(f"       Resultados del Análisis de {titulo}")
    print("="*50)
    print(f"➡️ Provincia con valor MÁXIMO: {max_min_data['max_provincia']} (Total: {max_min_data['max_valor']:,})")
    print(f"⬅️ Provincia con valor MÍNIMO: {max_min_data['min_provincia']} (Total: {max_min_data['min_valor']:,})")
    print("="*50 + "\n")


def grafico_acumulados_dia_cli(titulo: str, df_dia: pd.DataFrame, metrica: str):
    """
    Genera y muestra un gráfico de barras (Seaborn) de acumulados por día
    para la versión CLI.
    """
    if df_dia.empty:
        print(f"AVISO: No hay datos para mostrar el gráfico de {titulo}.")
        return

    plt.figure(figsize=(10, 6))
    
    # 1. Crear el gráfico de barras con Seaborn
    sns.barplot(
        x='dia_semana', 
        y=metrica, 
        data=df_dia, 
        palette='viridis',
        hue='dia_semana',
        legend=False,
        hue_order=df_dia['dia_semana'].tolist()
    )
    
    # 2. Configuración de títulos y etiquetas
    plt.title(f"Total Acumulado de {titulo} por Día de la Semana", fontsize=16)
    plt.xlabel('Día de la Semana', fontsize=12)
    plt.ylabel(f'Total Acumulado ({titulo})', fontsize=12)
    plt.xticks(rotation=45, ha='right') # Rotar etiquetas para mejor lectura
    
    plt.tight_layout() # Ajustar el diseño
    
    # 3. Mostrar la ventana de Matplotlib
    print("Mostrando Gráfico Acumulado Diario en una ventana de escritorio...")
    plt.show()


def grafico_queso_provincia_cli(titulo: str, df_provincia_total: pd.DataFrame, metrica: str):
    """
    Genera y muestra un gráfico de tarta (Matplotlib) de distribución por provincia
    y muestra el resumen de max/min en la terminal.
    """
    if df_provincia_total.empty:
        print(f"AVISO: No hay datos para mostrar el gráfico de {titulo}.")
        return

    # 1. Calcular el resumen de Max/Min usando el Modelo
    max_min_data = obtener_max_min_provincia(df_provincia_total, metrica)
    mostrar_mensaje_resumen(titulo, max_min_data)

    # 2. Preparar los datos y la figura
    plt.figure(figsize=(10, 10))
    
    # Extraer valores y etiquetas
    valores = df_provincia_total[metrica]
    etiquetas = df_provincia_total['province']
    
    # 3. Crear el gráfico de tarta (pie)
    plt.pie(
        valores, 
        labels=etiquetas, # type: ignore
        autopct='%1.1f%%', # Formato para mostrar el porcentaje en la tarta
        startangle=90,
        wedgeprops={'edgecolor': 'black', 'linewidth': 0.7}
    )
    
    # 4. Configuración
    plt.title(f"Distribución Total de {titulo} por Provincia", fontsize=16)
    plt.axis('equal') # Asegura que el gráfico es un círculo
    
    # 5. Mostrar la ventana de Matplotlib
    print("Mostrando Gráfico Tarta por Provincia en una ventana de escritorio...")
    plt.show()