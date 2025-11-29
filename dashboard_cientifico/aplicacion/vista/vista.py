import streamlit as st


def introduccion_general():
    st.subheader("Menú principal")
    st.markdown(
    """
    Selecciona una opción en el menú lateral:
    <ul>
        <li><span style="font-family: 'Calibri', sans-serif; font-size: 1.1em;">Dashboard</span></li>
        <li><span style="font-family: 'Calibri', sans-serif; font-size: 1.1em;">Análisis</span></li>
        <li><span style="font-family: 'Calibri', sans-serif; font-size: 1.1em;">Datos</span></li>
    </ul>
    """,
    unsafe_allow_html=True)


def introduccion_inicial():
    st.header("Bienvenidos al Dashboard sobre los datos de Covid en la segunda mitad del año 2021")
    st.subheader("Carga de datos")
    st.markdown(
    """
    Esta pagína aparece cuando no hay datos disponibles en la base de datos:
    <ul>
        <li><span style="font-family: 'Calibri', sans-serif; font-size: 1.1em;">Porque es la carga inicial</span></li>
        <li><span style="font-family: 'Calibri', sans-serif; font-size: 1.1em;">Porque se ha borrado accidentalmente la base de datos</span></li>
        <li><span style="font-family: 'Calibri', sans-serif; font-size: 1.1em;">Porque se ha elegido la opción 'Reset datos' del menú 'Gestión de Datos' (en el siguiente menú)</li>
    </ul>

    <div style="font-size: 1.2em; color: #333333; margin-top: 15px; margin-bottom: 15px;">
        <b>Seleccionar en el menú lateral 'Carga inicial' y pulsar el botón 'Cargar datos'</b>
    </div>

    <p>Aparecera a continuación la información del proceso</p>
   
    """,
    unsafe_allow_html=True)


def mostrar_mensajes_y_continuar(clave_num, clave_del, clave_exp):
    
    num_f = st.session_state[clave_num]
    datos_d = st.session_state[clave_del]
    datos_e = st.session_state[clave_exp]
    
    mensaje_mostrado = False
    
    if num_f:
        st.success(num_f)
        mensaje_mostrado = True
    if datos_e:
        st.success(datos_e)
        mensaje_mostrado = True
    if datos_d:
        st.warning(datos_d)
        mensaje_mostrado = True
        
    if mensaje_mostrado:
        if st.button("Continuar...", type='primary', key="btn_continuar_gestion"):
            st.session_state[clave_num] = ""
            st.session_state[clave_del] = ""
            st.session_state[clave_exp] = ""
            
            st.session_state['gestion_datos'] = False
            st.session_state['menu_refresh_key'] += 1
            st.rerun()


def mostrar_mensaje_con_continuacion(clave_mensaje: str, clave_terminada: str): 
    mensaje = st.session_state.get(clave_mensaje, "")
    
    if mensaje:
        if "Aviso:" in mensaje:
            st.warning(mensaje)
        elif "Error" in mensaje:
            st.error(mensaje)
        else:
            st.success(mensaje)
        
        st.session_state[clave_mensaje] = "" 
        
        # 3. Lógica de Rerun (Control de Flujo)
        # Esto reemplaza el botón "Continuar..."
        if st.session_state.get(clave_terminada, False):
            st.session_state[clave_terminada] = False # Limpiamos la bandera de terminado
            st.session_state['menu_refresh_key'] += 1

            st.session_state['eliminar_datos'] = False
            st.session_state['reset_datos'] = False
            st.rerun()