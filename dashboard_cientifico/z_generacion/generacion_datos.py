import pandas as pd
import numpy as np
from datetime import date, timedelta
from pathlib import Path

# --- CONFIGURACIÓN ---
NOMBRE_ARCHIVO_ORIGINAL = "datos_covid.csv" 
NOMBRE_ARCHIVO_SALIDA = "datos_covid_diciembre_2021.csv"
MES_A_GENERAR = 12  # Junio
AÑO_A_GENERAR = 2021
DIAS_DEL_MES = 31  # Junio tiene 30 días

def generar_datos_simulados(archivo_original: str, archivo_salida: str):
    """
    Genera un archivo CSV simulado para junio de 2021, manteniendo la coherencia 
    geográfica de ine_code y ccaa.
    """
    try:
        # 1. Cargar el DataFrame original y limpiar nombres de columna
        df_original = pd.read_csv(archivo_original, sep=',')
        df_original.columns = df_original.columns.str.strip()
        
        # 2. Identificar columnas. Las columnas de datos son todas menos las de identificación
        columnas_identificacion = ['date', 'province', 'ine_code', 'ccaa', 'source_name', 'source', 'comments']
        
        # Filtramos para tener la lista exacta de columnas de datos (casos, hospitalizados, etc.)
        columnas_datos = [col for col in df_original.columns if col not in columnas_identificacion]
        
        # 3. Mapeo Geográfico Estático
        # Creamos un mapeo Provincia -> (ine_code, ccaa) para asignar correctamente después
        mapeo_geografico = df_original[['province', 'ine_code', 'ccaa']].drop_duplicates().set_index('province')
        
        # 4. Generar la estructura base para el nuevo mes (Junio 2021)
        provincias = df_original['province'].unique()
        fechas_junio = [
            (date(AÑO_A_GENERAR, MES_A_GENERAR, 1) + timedelta(days=i)).strftime('%Y-%m-%d')
            for i in range(DIAS_DEL_MES)
        ]

        df_nuevo = pd.DataFrame([
            {'date': fecha, 'province': provincia}
            for fecha in fechas_junio for provincia in provincias
        ])
        
        # 5. Aplicar Muestreo Aleatorio (Sampling) SÓLO a las columnas de datos
        
        # Creamos un DataFrame solo con los valores a muestrear
        df_valores_a_samplear = df_original[columnas_datos]
        
        # Seleccionamos índices aleatorios con reemplazo, del tamaño del nuevo DataFrame
        indices_aleatorios = np.random.choice(df_valores_a_samplear.index, size=len(df_nuevo))
        
        # Copiamos los datos muestreados a las columnas del nuevo DataFrame
        df_nuevo[columnas_datos] = df_valores_a_samplear.loc[indices_aleatorios].reset_index(drop=True)
        
        # 6. Reasignar Identificadores Geográficos
        # Asignamos ine_code y ccaa en base al mapeo estático de la provincia
        df_nuevo = df_nuevo.merge(mapeo_geografico, on='province', how='left')
        
        # 7. Rellenar las columnas restantes (si las hubiera, como source o comments)
        # Tomamos la primera fila aleatoria de las columnas de comentarios y las rellenamos
        # Esto es solo por consistencia estructural.
        for col in ['source_name', 'source', 'comments']:
            if col in df_original.columns:
                 df_nuevo[col] = df_original[col].iloc[0]

        # 8. Ordenar las columnas finales y guardar el CSV
        columnas_finales = df_original.columns
        df_nuevo = df_nuevo[columnas_finales]
        
        ruta_salida = Path(archivo_salida)
        df_nuevo.to_csv(ruta_salida, index=False)
        
        print(f"🎉 Éxito: Se ha generado el archivo '{ruta_salida.name}' con {len(df_nuevo)} filas.")

    except FileNotFoundError:
        print(f"❌ Error: El archivo original '{archivo_original}' no fue encontrado.")
    except Exception as e:
        print(f"❌ Error durante la generación de datos: {type(e).__name__}: {e}")

# -------------------------------------------------------------

if __name__ == '__main__':
    generar_datos_simulados(NOMBRE_ARCHIVO_ORIGINAL, NOMBRE_ARCHIVO_SALIDA)