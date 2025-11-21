import streamlit as st
import pandas as pd
from pathlib import Path
# Asumimos que 'obtener_datos_db' es la función que modificaste antes
from .tu_modulo_modelo import obtener_datos_db 

# Clave que usaremos para almacenar el DataFrame
CLAVE_DATAFRAME = 'datos_principales' 
RUTA_DB = Path('ruta/a/tu/db.db') 

def inicializar_dataframe():
    """Carga el DataFrame de la DB y lo almacena en st.session_state."""
    
    # Solo cargar si la clave NO existe en el estado de sesión
    if CLAVE_DATAFRAME not in st.session_state:
        # Llama a la función que obtiene los datos
        df = obtener_datos_db(RUTA_DB) 
        
        # Almacena el DataFrame en la sesión
        st.session_state[CLAVE_DATAFRAME] = df
        
        # Opcional: Almacenar un indicador de que el DF está vacío o listo
        if df.empty:
            st.session_state['datos_cargados'] = False
            # Puedes mostrar un mensaje de error aquí
        else:
            st.session_state['datos_cargados'] = True



# -------------------------------------------------------------
# LLAMADA AL INICIO DEL SCRIPT
# -------------------------------------------------------------
# Llama a esta función inmediatamente después de las importaciones
inicializar_dataframe()


# Accede al DataFrame en cualquier función de tu aplicación
df_trabajo = st.session_state[CLAVE_DATAFRAME]

if st.session_state['datos_cargados']:
    # Crea un gráfico usando los datos persistentes
    st.line_chart(df_trabajo['columna_interes'])
else:
    st.error("No se pudieron cargar los datos. Verifique la base de datos.")