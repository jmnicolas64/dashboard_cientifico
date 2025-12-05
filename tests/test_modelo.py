# tests/test_modelo.py
import pandas as pd
from dashboard_cientifico.aplicacion.modelo.carga_datos import obtener_datos_completos

def test_obtener_datos_completos_devuelve_df():
    """Verifica que la funcion devuelve un DataFrame de pandas."""
    df = obtener_datos_completos()
    assert isinstance(df, pd.DataFrame)

def test_obtener_datos_completos_no_vacio():
    """Verifica que el DataFrame no está vacío."""
    df = obtener_datos_completos()
    assert not df.empty