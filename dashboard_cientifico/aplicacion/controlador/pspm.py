mensaje_a_mostrar_inicial = st.session_state['mensajes_carga_inicial']
if mensaje_a_mostrar_inicial:
    st.info(mensaje_a_mostrar_inicial)
    
    st.session_state['mensajes_carga_inicial'] = "" 
    
    if st.button("Continuar...", type='primary', key="btn_continuar_inicial"):
        st.session_state['menu_refresh_key'] += 1
        st.rerun()

mensaje_a_mostrar_elim = st.session_state['mensaje_eliminacion']
if mensaje_a_mostrar_elim:

    if "Aviso:" in mensaje_a_mostrar_elim:
        st.warning(mensaje_a_mostrar_elim)

    elif "Error:" in mensaje_a_mostrar_elim:
        st.error(mensaje_a_mostrar_elim)

    else:
        st.success(mensaje_a_mostrar_elim)
    
    st.session_state['mensaje_eliminacion'] = "" 
    
    if st.button("Continuar...", type='primary', key="btn_continuar_elim"):
        st.session_state['menu_refresh_key'] += 1
        st.rerun()