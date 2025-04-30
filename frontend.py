import streamlit as st
import requests

st.title('Predicción de Precios de Casas en Boston')

# Formulario para ingresar datos
with st.form("formulario_prediccion"):
    zn = st.number_input("ZN - % de zonas residenciales", value=0.0, step=0.0001, format="%.4f")
    indus = st.number_input("INDUS - % de negocios no minoristas", value=0.0, step=0.0001, format="%.4f")
    rm = st.number_input("RM - Número promedio de habitaciones", value=6.0, step=0.0001, format="%.4f")
    ptratio = st.number_input("PTRATIO - Ratio alumnos/profesor", value=15.0, step=0.0001, format="%.4f")
    b = st.number_input("BLACK - 1000(Bk - 0.63)^2", value=400.0, step=0.0001, format="%.4f")
    lstat = st.number_input("LSTAT - % población de bajo ingreso", value=12.0, step=0.0001, format="%.4f")
    submit = st.form_submit_button('Predecir')

if submit:
    datos = {
       "zn": zn, "indus": indus, "rm": rm,
        "ptratio": ptratio, "b": b, "lstat": lstat
    }
    try:
        respuesta = requests.post("http://localhost:8000/predict/", json=datos)
        if respuesta.status_code == 200:
            prediccion = respuesta.json()
            st.success(f"Precio estimado: ${prediccion['prediction']:.2f} mil dólares")
        else:
            st.error(f"Error en la API: {respuesta.text}")
    except Exception as e:
        st.error(f"No se pudo conectar al servidor API. Error: {str(e)}")
        st.info("Asegúrate de que la API FastAPI esté corriendo en http://localhost:8000")