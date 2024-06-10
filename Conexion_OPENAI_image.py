import streamlit as st
import os
from openai import OpenAI
# Inicialización del cliente OpenAI con la clave API desde las variables de entorno
client=OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Campo de entrada de Streamlit para que el usuario introduzca su pregunta
option=st.selectbox(
    "Elija una opción",
    ("Texto","Imagen")
)
# Verifica que se haya ingresado un mensaje antes de realizar la solicitud
st.write("Has eligido", option)