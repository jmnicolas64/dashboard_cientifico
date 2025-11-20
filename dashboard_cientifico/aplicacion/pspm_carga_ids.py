import json
from pathlib import Path

# 1. Diccionario de IDs de Carga
CARGA_ID_POSIBLES = {
    "Mayo 2021": "202105",
    "Junio 2021": "202106",
    "Julio 2021": "202107",
    "Agosto 2021": "202108",
    "Septiembre 2021": "202109",
    "Octubre 2021": "202110",
    "Noviembre 2021": "202111",
    "Diciembre 2021": "202112"
}

# 2. Nombre del archivo de salida
NOMBRE_ARCHIVO_SALIDA = "carga_ids.json"

def generar_json_ids():
    """Escribe el diccionario CARGA_ID_POSIBLES en un archivo JSON."""
    
    ruta_salida = Path(NOMBRE_ARCHIVO_SALIDA)
    
    try:
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            json.dump(CARGA_ID_POSIBLES, f, ensure_ascii=False, indent=4)
        
        print(f"🎉 Éxito: El archivo '{NOMBRE_ARCHIVO_SALIDA}' se ha generado correctamente en {ruta_salida.resolve()}")

    except IOError as e:
        print(f"❌ Error al escribir el archivo: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

# -------------------------------------------------------------
## 🚀 Bloque de Ejecución Principal
# -------------------------------------------------------------

if __name__ == '__main__':
    generar_json_ids()