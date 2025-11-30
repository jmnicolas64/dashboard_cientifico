    col1, col2, col3 = st.columns(3)

    with col1:
        # Usamos f-strings para formatear el texto
        st.write(f"**Cargar CSV:** `{st.session_state['cargar_nuevo_csv']}`")
        st.write(f"**gestion terminada:** `{st.session_state['gestion_terminada']}`")
        
    with col2:
        st.write(f"**Eliminar Datos:** `{st.session_state['eliminar_datos']}`")
        st.write(f"**eliminacion terminada:** `{st.session_state['eliminacion_terminada']}`")

    with col3:
        st.write(f"**Reset Datos:** `{st.session_state['reset_datos']}`")