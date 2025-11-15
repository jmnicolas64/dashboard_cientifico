# C:\...\vista\version_basica\vista_graficos.py
import matplotlib.pyplot as plt
import seaborn as sns
# Importa la configuración para imprimir los títulos de los menús
from aplicacion.config.settings import OPCIONES_GRAFICOS 

plt.ion() # Modo interactivo


def mostrar_menu_principal():
    print("\n" + "#"*60)
    print("         💻 PROYECTO FINAL 3: DASHBOARD CIENTÍFICO")
    print("#"*60)
    print("1. Ejecutar Ejercicio 1 (Procesar CSV -> Guardar JSON)")
    print("2. Ejecutar Ejercicio 2 (Gráficas de Barras por Provincia)")
    print("3. Ejecutar Ejercicio 3 (Análisis de Extremos y Gráficas de Queso)")
    print("4. Salir del Programa")
    print("="*60)

def mostrar_menu_ejercicio_secundario(titulo):
    print("\n" + "═"*50)
    print(f"📊 MENÚ EJERCICIO: {titulo}")
    for num, op in OPCIONES_GRAFICOS.items():
        print(f"{num}. {op['nombre']}")
    print("5. Volver al Menú Principal")
    print("═"*50)


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


# EJEMPLO DE MEJORA EN UN GRÁFICO DE QUESO ESTÁNDAR
def generar_grafica_queso(totales_por_provincia, metrica, provincia_max, provincia_min):
    """
    Genera un gráfico de queso visualmente mejorado usando estilos de Seaborn,
    enfatizando el máximo y el mínimo mediante 'explode' y paletas de color.
    """
    # 1. Preparación de datos (Se mantiene la lógica de Extremos vs Resto)
    valor_max = totales_por_provincia[provincia_max]
    valor_min = totales_por_provincia[provincia_min]
    total_general = sum(totales_por_provincia.values())
    valor_resto = total_general - valor_max - valor_min
    
    etiquetas = [
        f'{provincia_max} (Máx: {valor_max})', 
        f'{provincia_min} (Mín: {valor_min})', 
        f'Resto de Provincias ({valor_resto})'
    ]
    datos = [valor_max, valor_min, valor_resto]
    
    titulo_limpio = metrica.replace('_', ' ').title()
    titulo = f'Distribución de {titulo_limpio} (Extremos vs Resto)'

    # 2. Configuración y Dibujo del Gráfico
    
    # 📈 Aplicar un estilo de Seaborn (mejora fuentes y fondo)
    sns.set_style("whitegrid") 
    plt.figure(figsize=(10, 10)) 

    # 💥 EXPLODE: Separa la porción del máximo (0.1) y del mínimo (0.05) para dar énfasis.
    explode = (0.1, 0.05, 0)
    
    # 🌈 PALETA: Usamos una paleta de Seaborn (ej: 'Set2' o 'Pastel1')
    # Se genera un conjunto de 3 colores.
    colores = sns.color_palette('pastel', n_colors=3) 
    
    plt.pie(
        datos, 
        labels=etiquetas, 
        autopct='%1.1f%%',       # Muestra el porcentaje con un decimal
        startangle=90, 
        wedgeprops={'edgecolor': 'black', 'linewidth': 1.5}, # Borde negro para definir las porciones
        explode=explode,  # Aplica la separación
        colors=colores,   # Aplica los colores de Seaborn
        # Sombra sutil para darle profundidad
        shadow=True 
    )
    
    plt.title(titulo, fontsize=16, fontweight='bold')
    plt.axis('equal') 
    plt.show() 
    
    # Manejo del modo interactivo
    input("Presiona ENTER para volver al menú...")
    plt.close()