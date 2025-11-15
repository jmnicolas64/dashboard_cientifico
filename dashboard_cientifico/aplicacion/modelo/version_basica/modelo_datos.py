import csv
import json
import os
from datetime import datetime

# Importaciones desde tu carpeta de configuración
from aplicacion.config.settings import (
    NOMBRE_CSV, NOMBRE_JSON, METRICAS_MAPEO, 
    METRICAS_CLAVES, DIAS_SEMANA
)


# =====================================================================
# EJERCICIO 1: Procesamiento CSV y Guardado JSON (ADAPTADO)
# =====================================================================

def obtener_dia_semana(fecha_str):
    """Convierte una cadena de fecha (YYYY-MM-DD) al nombre del día de la semana."""
    try:
        # Asumiendo formato 'YYYY-MM-DD' (ISO 8601)
        fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d')
        # weekday() devuelve 0 para Lunes, 6 para Domingo.
        indice_dia = fecha_obj.weekday()
        return DIAS_SEMANA[indice_dia]
    except ValueError:
        # Devuelve un valor que no se usará si la fecha es inválida
        return "Desconocido"

def procesar_datos_csv(nombre_archivo_csv, nombre_archivo_json):
    """
    Lee un CSV (adaptado), agrupa métricas por 'province' y día de la semana, 
    y guarda el resultado en JSON.
    """
    datos_agrupados = {}
    print(f"Iniciando procesamiento del archivo: {nombre_archivo_csv}...")
    
    try:
        with open(nombre_archivo_csv, mode='r', encoding='utf-8') as archivo_csv:
            lector = csv.DictReader(archivo_csv)
            
            for fila in lector:
                try:
                    # Usamos 'province' del CSV
                    provincia = fila['province']
                    
                    # Generamos el 'dia_semana' a partir de la columna 'date'
                    dia = obtener_dia_semana(fila['date'])
                    
                    if dia == "Desconocido":
                        continue # Saltamos filas con formato de fecha incorrecto

                    if provincia not in datos_agrupados:
                        # Inicializa la estructura para la nueva provincia
                        datos_agrupados[provincia] = {
                            d: {m: 0 for m in METRICAS_CLAVES} for d in DIAS_SEMANA
                        }
                    
                    # Acumular los datos. 
                    for metrica_proyecto, columna_csv in METRICAS_MAPEO.items():
                        # Convertir a entero y acumular (usando el nombre de columna del CSV)
                        valor = int(fila.get(columna_csv, 0) or 0) # Aseguramos 0 si es None o vacío
                        datos_agrupados[provincia][dia][metrica_proyecto] += valor
                        
                except ValueError:
                    # Esto ocurre si hay datos no numéricos/vacíos en las columnas de métricas
                    pass 
                except KeyError as e:
                    print(f"Error fatal: Columna {e} no encontrada en el CSV. El CSV debe tener 'province', 'date' y las columnas de métricas.")
                    return None
                    
    except FileNotFoundError:
        print(f"¡Error! El archivo '{nombre_archivo_csv}' no fue encontrado. Asegúrate de que está en la carpeta de trabajo.")
        return None
        
    # Guardar en JSON
    try:
        with open(nombre_archivo_json, 'w', encoding='utf-8') as archivo_json:
            json.dump(datos_agrupados, archivo_json, indent=4)
        print(f"✅ ¡Éxito! Datos agrupados guardados en '{nombre_archivo_json}'.")
    except Exception as e:
        print(f"Error al guardar el archivo JSON: {e}")
        
    return datos_agrupados

# =====================================================================
# FUNCIONES COMUNES y EJERCICIOS 2 y 3 (SIN CAMBIOS DE LÓGICA)
# =====================================================================

def cargar_datos(nombre_archivo):
    """Carga los datos agrupados desde el archivo JSON."""
    if not os.path.exists(nombre_archivo):
        print(f"❌ Error: El archivo '{nombre_archivo}' no existe. Ejecuta primero la Opción 1.")
        return None
        
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
            return datos
    except json.JSONDecodeError:
        print(f"❌ Error: No se pudo decodificar el JSON del archivo '{nombre_archivo}'.")
        return None

def calcular_totales_y_extremos(datos, metrica):
    """
    Calcula el total de una métrica para cada provincia y encuentra los extremos.
    """
    totales_por_provincia = {}
    for provincia, datos_provincia in datos.items():
        # Usa METRICAS_CLAVES para iterar
        total_metrica = sum(dia.get(metrica, 0) for dia in datos_provincia.values())
        totales_por_provincia[provincia] = total_metrica

    if not totales_por_provincia:
        return {}, None, None

    provincia_max = max(totales_por_provincia, key=totales_por_provincia.get) # type: ignore
    provincia_min = min(totales_por_provincia, key=totales_por_provincia.get) # type: ignore

    return totales_por_provincia, provincia_max, provincia_min