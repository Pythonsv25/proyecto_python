import streamlit as st
import requests
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Predicción de Precios en Boston",
    page_icon="🏠",
    layout="wide"
)


API_URL = "https://boston-housing-api.onrender.com/predict"

# Título y descripción
st.title("🏠 Predicción de Precios de Viviendas en Boston")
st.markdown("""
Predice el valor mediano de viviendas usando el modelo de Machine Learning.
Ingresa los valores requeridos y haz clic en **Predecir**.
""")

# Sidebar con información
with st.sidebar:
    st.header("ℹ️ Instrucciones")
    st.markdown("""
    1. Completa todos los campos del formulario
    2. Haz clic en el botón **Predecir**
    3. Mira el resultado en la sección inferior
    """)
    st.divider()
    st.markdown("**Variables:**")
    st.markdown("- ZN: % de zonas residenciales")
    st.markdown("- INDUS: % de negocios no minoristas")
    st.markdown("- RM: Número promedio de habitaciones")
    st.markdown("- PTRATIO: Ratio alumnos/profesor")
    st.markdown("- B: Proporción de población afroamericana")
    st.markdown("- LSTAT: % de población de bajo estatus")

# Formulario de entrada
with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        zn = st.number_input("ZN - % de zonas residenciales", min_value=0.0, max_value=100.0, value=25.0, step=0.1)
        indus = st.number_input("INDUS - % de negocios no minoristas", min_value=0.0, max_value=30.0, value=5.0, step=0.1)
        rm = st.number_input("RM - Número promedio de habitaciones", min_value=3.0, max_value=9.0, value=6.0, step=0.1)
    
    with col2:
        ptratio = st.number_input("PTRATIO - Ratio alumnos/profesor", min_value=12.0, max_value=23.0, value=15.0, step=0.1)
        b = st.number_input("B - Proporción de población afroamericana", min_value=0.0, max_value=400.0, value=350.0, step=1.0)
        lstat = st.number_input("LSTAT - % población de bajo estatus", min_value=1.0, max_value=40.0, value=12.0, step=0.1)
    
    submitted = st.form_submit_button("✨ Predecir Precio")

# Procesamiento de la predicción
if submitted:

    input_data = {
        "zn": float(zn),
        "indus": float(indus),
        "rm": float(rm),
        "ptratio": float(ptratio),
        "b": float(b),
        "lstat": float(lstat)
    }
    
    try:
        # Muestra un spinner mientras se hace la petición
        with st.spinner("Calculando predicción..."):
            response = requests.post(API_URL, json=input_data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            prediction = result.get("prediction", 0)
            
            
            st.success("### Resultado de la Predicción")
            st.metric(label="**Precio Mediano Estimado**", value=f"${prediction:,.2f} mil")
            
            
            st.divider()
            st.subheader("📊 Datos de Entrada")
            input_df = pd.DataFrame([input_data])
            st.dataframe(input_df.T.rename(columns={0: "Valor"}), use_container_width=True)
            
        else:
            st.error(f"Error en la API: {response.text}")
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {str(e)}")
        st.info("⚠️ Si la API está en Render Free, puede estar 'dormida'. Espera 20-30 segundos e intenta nuevamente.")


st.divider()
st.markdown("""
🔍 **Nota:** Este modelo fue entrenado con datos del dataset Boston Housing.
Los resultados son estimaciones y no deben considerarse como valores exactos.
""")
