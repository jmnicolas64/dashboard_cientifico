import csv
import json
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime # ¡Necesario para convertir la fecha a día de la semana!

plt.ion()

# --- CONFIGURACIÓN DE ARCHIVOS Y METRICAS ---
NOMBRE_CSV = 'datos_covid.csv'
NOMBRE_JSON = 'datos_agrupados.json'

# Mapeo de las métricas del proyecto a las columnas del CSV
METRICAS_MAPEO = {
    'num_def': 'deceased',
    'new_cases': 'new_cases',
    'num_hosp': 'num_hosp',
    'num_uci': 'num_uci'
}
METRICAS_CLAVES = list(METRICAS_MAPEO.keys()) # ['num_def', 'new_cases', ...]

DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

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

def generar_grafica_barras(datos, metrica):
    """
    Genera una gráfica de barras utilizando Seaborn para un estilo moderno.
    datos: Diccionario de datos procesados.
    metrica: La columna que se desea acumular (ej: 'num_casos').
    """
    # 1. Preparación de datos: Calcular el total por provincia
    provincias = []
    valores_totales = []
    
    for provincia, dias in datos.items():
        total = sum(dia.get(metrica, 0) for dia in dias.values())
        provincias.append(provincia)
        valores_totales.append(total)

    # 2. Configuración y Dibujo del Gráfico
    
    # Aplicar un estilo de Seaborn (opcional, pero mejora la estética)
    sns.set_style("whitegrid") 
    
    plt.figure(figsize=(14, 7))
    
    # --- CAMBIO CLAVE: Usar sns.barplot() ---
    
    # x: Provincias, y: Valores. Usamos 'viridis' para una paleta moderna.
    sns.barplot(
        x=provincias, 
        y=valores_totales, 
        palette='viridis', 
        edgecolor='black' # Añade un borde sutil
    )
    
    # 3. Personalización (Usando funciones de Matplotlib que siguen funcionando)
    titulo_limpio = metrica.replace('_', ' ').title()
    plt.title(f'Acumulado de {titulo_limpio} por Provincia', fontsize=16, fontweight='bold')
    plt.xlabel('Provincia', fontsize=12)
    plt.ylabel(f'Total de {titulo_limpio}', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def menu_ejercicio2(datos):
    """Menú interactivo para las gráficas de barras (Ejercicio 2)."""
    OPCIONES = {
        1: {'metrica': 'num_def', 'nombre': 'Defunciones'},
        2: {'metrica': 'new_cases', 'nombre': 'Casos'},
        3: {'metrica': 'num_hosp', 'nombre': 'Hospitalizados'},
        4: {'metrica': 'num_uci', 'nombre': 'UCI'}
    }
    while True:
        print("\n" + "═"*50)
        print("📊 MENÚ EJERCICIO 2: GRÁFICAS DE BARRAS POR PROVINCIA")
        for num, op in OPCIONES.items():
            print(f"{num}. {op['nombre']}")
        print("5. Volver al Menú Principal")
        print("═"*50)
        
        opcion = input("Introduce tu elección (1-5): ")
        if opcion == '5': break
        
        try:
            opcion_int = int(opcion)
            if opcion_int in OPCIONES:
                generar_grafica_barras(datos, OPCIONES[opcion_int]['metrica'])
            else:
                print("Opción no válida.")
        except ValueError:
            print("Entrada no válida.")

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

# EJEMPLO DE MEJORA EN UN GRÁFICO DE QUESO ESTÁNDAR
def generar_grafica_queso(totales_por_provincia, metrica, provincia_max, provincia_min):
    """
    Genera un gráfico de queso para las provincias con mayor y menor valor, 
    y el resto agrupado.
    """
    
    # Obtener el valor de la provincia con máximo y mínimo
    valor_max = totales_por_provincia[provincia_max]
    valor_min = totales_por_provincia[provincia_min]
    
    # Calcular el resto (la suma de todas las demás provincias)
    total_general = sum(totales_por_provincia.values())
    
    # Restar los extremos para obtener la suma del 'Resto'
    valor_resto = total_general - valor_max - valor_min
    
    # 1. Definir los datos para el pie chart
    etiquetas = [
        f'{provincia_max} (Máximo)', 
        f'{provincia_min} (Mínimo)', 
        'Resto de Provincias'
    ]
    datos = [valor_max, valor_min, valor_resto]
    
    titulo_limpio = metrica.replace('_', ' ').title()
    titulo = f'Distribución de {titulo_limpio} (Extremos vs Resto)'

    # 2. Dibujar el Gráfico
    sns.set_style("whitegrid") 
    plt.figure(figsize=(9, 9))
    
    plt.pie(
        datos, 
        labels=etiquetas, 
        autopct='%1.1f%%',       # Muestra el porcentaje con un decimal
        startangle=90, 
        wedgeprops={'edgecolor': 'black', 'linewidth': 1.5}
    )
    
    plt.title(titulo, fontsize=16, fontweight='bold')
    plt.axis('equal') 
    plt.show() # Mantener plt.show()
    
    # Añadido: Espera de usuario para no bloquear el menú
    input("Presiona ENTER para volver al menú...")
    plt.close() # Cierra la ventana del gráfico al volver al menú

def menu_ejercicio3(datos):
    """Menú interactivo para el análisis de extremos (Ejercicio 3)."""
    OPCIONES = {
        1: {'metrica': 'num_def', 'nombre': 'Defunciones'},
        2: {'metrica': 'new_cases', 'nombre': 'Casos'},
        3: {'metrica': 'num_hosp', 'nombre': 'Hospitalizados'},
        4: {'metrica': 'num_uci', 'nombre': 'UCI'}
    }
    while True:
        print("\n" + "═"*50)
        print("🍕 MENÚ EJERCICIO 3: ANÁLISIS DE EXTREMOS Y GRÁFICAS DE QUESO")
        for num, op in OPCIONES.items():
            print(f"{num}. {op['nombre']}")
        print("5. Volver al Menú Principal")
        print("═"*50)
        
        opcion = input("Introduce tu elección (1-5): ")
        if opcion == '5': break
        
        try:
            opcion_int = int(opcion)
            if opcion_int in OPCIONES:
                metrica_clave = OPCIONES[opcion_int]['metrica']
                totales, p_max, p_min = calcular_totales_y_extremos(datos, metrica_clave)
                generar_grafica_queso(totales, metrica_clave, p_max, p_min) # type: ignore
            else:
                print("Opción no válida.")
        except ValueError:
            print("Entrada no válida.")

# =====================================================================
# MENÚ PRINCIPAL DEL PROYECTO
# =====================================================================

def menu_principal():
    """Menú principal para elegir la ejecución de los ejercicios."""

    datos_agrupados = None
    
    while True:
        print("\n" + "#"*60)
        print("         💻 PROYECTO FINAL 3: DASHBOARD CIENTÍFICO")
        print("#"*60)
        print("1. Ejecutar Ejercicio 1 (Procesar CSV -> Guardar JSON)")
        print("2. Ejecutar Ejercicio 2 (Gráficas de Barras por Provincia)")
        print("3. Ejecutar Ejercicio 3 (Análisis de Extremos y Gráficas de Queso)")
        print("4. Salir del Programa")
        print("="*60)
        
        opcion = input("Selecciona una opción (1-4): ")
        
        if opcion == '1':
            datos_agrupados = procesar_datos_csv(NOMBRE_CSV, NOMBRE_JSON)
        
        elif opcion == '2':
            if datos_agrupados is None:
                datos_agrupados = cargar_datos(NOMBRE_JSON)
            
            if datos_agrupados:
                menu_ejercicio2(datos_agrupados)
            
        elif opcion == '3':
            if datos_agrupados is None:
                datos_agrupados = cargar_datos(NOMBRE_JSON)
                
            if datos_agrupados:
                menu_ejercicio3(datos_agrupados)
                
        elif opcion == '4':
            print("Programa finalizado. ¡Hasta pronto!")
            break
            
        else:
            print("Opción no válida. Por favor, introduce un número del 1 al 4.")


# --- EJECUCIÓN PRINCIPAL DEL SCRIPT ---
if __name__ == "__main__":
    menu_principal()