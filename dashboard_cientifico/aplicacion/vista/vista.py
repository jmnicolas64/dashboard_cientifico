import streamlit as st


def introduccion_general():
    st.markdown(
    """
    El orden de ejecucion es el siguiente:
    <ol>
        <li><span style="font-family: 'Calibri', sans-serif; font-size: 1.1em;">Cargar excel original</span></li>
        <li><span style="font-family: 'Calibri', sans-serif; font-size: 1.1em;">Configurar semana</span></li>
        <li><span style="font-family: 'Calibri', sans-serif; font-size: 1.1em;">Agrupar</span></li>
    </ol>

    <b>Antes de seleccionar la opción 'Cargar excel original' hay que asegurarse de lo siguiente:</b>
    <ol>
        <li><span style="font-family: 'Calibri', sans-serif; font-size: 1.1em;">
            El archivo excel original esta en la carpeta './archivos', se llama 'confemetal.xlsx' y la hoja a leer se llama 'confemetal'</span></li>
        <li><span style="font-family: 'Calibri', sans-serif; font-size: 1.1em;">
            El archivo 'configuración.py' tiene la funcion 'semana_y_año()' bien configurada </span></li>
    </ol>    
    """,
    unsafe_allow_html=True)