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


def mostrar_tabla_resumen_cli(df: pd.DataFrame, titulo: str):
    if df.empty:
        print(f"AVISO: La tabla de resumen '{titulo}' está vacía.")
        return

    print("\n" + "-"*50)
    print(f"\nRESUMEN DE DATOS PARA EL GRÁFICO DE {titulo.upper()}\n")

    df_mostrar = df.copy()

    df_mostrar = df_mostrar.rename(columns={
        'province': 'PROVINCIA',
        'porcentaje': 'PORCENTAJE',
        df_mostrar.columns[1]: 'TOTAL'
    })

    df_mostrar['TOTAL'] = df_mostrar['TOTAL'].apply(lambda x: f"{int(x):,}")
    df_mostrar['PORCENTAJE'] = df_mostrar['PORCENTAJE'].apply(lambda x: f"{x:.2f}%")

    print(df_mostrar.to_string(index=False))


def mostrar_mensaje_resumen(titulo: str, max_min_data: Dict):
    print("\n" + "-"*50)
    print(f"\nRESULTADOS DEL ANÁLISIS DE {titulo}\n")
    print(f"Provincia con valor MÁXIMO: {max_min_data['max_provincia']} (Total: {max_min_data['max_valor']:,})")
    print(f"Provincia con valor MÍNIMO: {max_min_data['min_provincia']} (Total: {max_min_data['min_valor']:,})")


def grafico_acumulados_dia_cli(titulo: str, df_dia: pd.DataFrame, metrica: str):
    if df_dia.empty:
        print(f"AVISO: No hay datos para mostrar el gráfico de {titulo}.")
        return

    fig, ax = plt.subplots(figsize=(12, 7))
    
    sns.barplot(
        x='dia_semana', 
        y=metrica, 
        data=df_dia, 
        palette='viridis',
        hue='dia_semana',
        legend=False,
        hue_order=df_dia['dia_semana'].tolist(),
        ax=ax
    )

    for bar in ax.patches:
        valor = bar.get_height() # type: ignore
        x_pos = bar.get_x() + bar.get_width() / 2 # type: ignore
        offset = valor * 0.01 
        
        ax.text(
            x_pos,
            valor + offset,
            f"{int(valor):,}",
            ha='center',
            va='bottom',
            fontsize=10
        )

    ax.set_title(f"Total Acumulado de {titulo} por Día de la Semana", fontsize=16)
    ax.set_xlabel('Día de la Semana', fontsize=12)
    ax.set_ylabel(f'Total Acumulado ({titulo})', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.show()


def grafico_queso_provincia_cli(titulo: str, df_provincia_total: pd.DataFrame, metrica: str):
    if df_provincia_total.empty:
        print(f"AVISO: No hay datos para mostrar el gráfico de {titulo}.")
        return

    max_min_data = obtener_max_min_provincia(df_provincia_total, metrica)
    mostrar_tabla_resumen_cli(df_provincia_total, titulo)
    mostrar_mensaje_resumen(titulo, max_min_data)

    plt.figure(figsize=(10, 10))

    valores = df_provincia_total[metrica]
    etiquetas = df_provincia_total['province']
  
    wedges, texts, autotexts =plt.pie( # type: ignore
        valores, 
        labels=None,
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops={'edgecolor': 'black', 'linewidth': 0.7}
    )

    plt.legend(
        wedges,
        etiquetas,
        title="Provincias",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1)
    )

    plt.title(f"Distribución Total de {titulo} por Provincia", fontsize=16)
    plt.axis('equal')

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