import streamlit as st

# 1. Inicialización de variables de estado
if 'refresh_key' not in st.session_state:
    st.session_state['refresh_key'] = 0

if 'message' not in st.session_state:
    st.session_state['message'] = ""
    
if 'step_done' not in st.session_state:
    st.session_state['step_done'] = False

st.title("Prueba de st.rerun y Claves")
st.markdown("---")

# ----------------------------------------------------
# ESCENARIO 1: EL SELECTOR QUE NO SE RESETEA (TU PROBLEMA)
# ----------------------------------------------------
st.header("1. Selector Sin Clave Dinámica (Mantiene estado)")

# Selector A: No tiene una clave única que cambie.
# Streamlit lo considera el "mismo widget" en cada rerun.
selection_A = st.selectbox(
    "Selector A (No se resetea):",
    ['Opción A1', 'Opción A2', 'Opción A3'],
    index=0
)
st.info(f"Selección A: {selection_A}")

# ----------------------------------------------------
# ESCENARIO 2: EL SELECTOR QUE SÍ SE RESETEA (LA SOLUCIÓN)
# ----------------------------------------------------
st.header("2. Selector Con Clave Dinámica (Se resetea)")

# Selector B: Su clave incluye 'refresh_key'.
# Cuando 'refresh_key' cambia, Streamlit lo ve como un 'nuevo widget'.
selection_B = st.selectbox(
    "Selector B (Se resetea):",
    ['Opción B1', 'Opción B2', 'Opción B3'],
    index=0,
    key=f"selector_b_{st.session_state['refresh_key']}" # CLAVE DINÁMICA
)
st.info(f"Selección B: {selection_B}")

st.markdown("---")

# ----------------------------------------------------
# LÓGICA DE BOTONES Y RERUN
# ----------------------------------------------------

def execute_action():
    """Simula una acción de carga de datos."""
    st.session_state['message'] = f"¡Acción completada! El Selector B se dibujará con la clave: {st.session_state['refresh_key'] + 1}"
    st.session_state['step_done'] = True
    
    # IMPORTANTE: El incremento de la clave debe hacerse ANTES del rerun
    # para que la siguiente ejecución ya vea la clave nueva.
    st.session_state['refresh_key'] += 1 
    st.rerun()

# Botón que simula la carga de datos
st.button("1. Ejecutar acción (Simula Cargar Datos)", on_click=execute_action)

# Se muestra un mensaje y el botón 'Continuar...'
if st.session_state['step_done']:
    st.success(st.session_state['message'])
    
    def reset_and_continue():
        """Resetea el estado y hace el RERUN final."""
        st.session_state['message'] = ""
        st.session_state['step_done'] = False
        
        # Opcional, pero recomendado para el RERUN final de limpieza
        st.session_state['refresh_key'] += 1 
        st.rerun()

    st.button("2. Continuar... (Simula Botón Final)", on_click=reset_and_continue, type='primary')

st.markdown(f"--- Clave de Refresco Actual: `{st.session_state['refresh_key']}` ---")
