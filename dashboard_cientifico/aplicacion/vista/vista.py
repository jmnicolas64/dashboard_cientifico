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

    st.success("success")
    st.warning ("warning")
    st.error("error")


def introduccion_inicial():
    st.header("Carga de datos")
    st.markdown(
    """
    Esta pagína aparece cuando no hay datos disponibles en la base de datos:
    <ul>
        <li><span style="font-family: 'Calibri', sans-serif; font-size: 1.1em;">Porque es la carga inicial</span></li>
        <li><span style="font-family: 'Calibri', sans-serif; font-size: 1.1em;">Porque se ha borrado accidentalmente la base de datos</span></li>
        <li><span style="font-family: 'Calibri', sans-serif; font-size: 1.1em;">Porque se ha elegido la opción 'Reset datos' del menú 'Gestión de Datos' (en el siguiente menú)</li>
    </ul>

    <b>Seleccionar en el menú lateral 'Carga inicial' y pulsar el botón 'Cargar datos'</b>

    <p>Aparecera a continuación la información del proceso</p>
   
    """,
    unsafe_allow_html=True)
