import streamlit as st
import os
from openai import OpenAI
# Inicialización del cliente OpenAI con la clave API desde las variables de entorno
client=OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Campo de entrada de Streamlit para que el usuario introduzca su pregunta
mensaje=st.text_input("Pregúntame lo que quieras")
# Verifica que se haya ingresado un mensaje antes de realizar la solicitud
if mensaje:
    chat_completions=client.chat.completions.create(
        messages=[
            {
                "role":"user",
                "content":mensaje

            }
        ],
        model="gpt-3.5-turbo",
    )
    if chat_completions.choices:
        st.write(chat_completions.choices[0].message.content)