import streamlit as st
from groq import Groq
st.set_page_config(page_title="IA Chat", page_icon="😎")

MODELOS = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

#Me conecta a la API, crear un usuario
def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key = clave_secreta)

def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model = modelo,
        messages = [{"role":"user", "content" : mensajeDeEntrada }],
        stream = True
    )


#Simula un historial de mensaje
def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []


def configurar_pagina():
    st.title("Mi chat con la IA")
    st.sidebar.title("Configuracion")
    opcion = st.sidebar.selectbox(
        "Elegi modelo",
        options = MODELOS,
        index = 0
    )
    return opcion 


def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append(
        {"role": rol, "content": contenido, "avatar": avatar}
    )


def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar = mensaje["avatar"]):
            st.markdown(mensaje["content"])

#Sector del chat en web
def area_chat():
    contenedorDelChat = st.container(height=400, border = True)
    with contenedorDelChat : mostrar_historial()

def generar_respuesta(chat_completo):
    respuesta_completa = " "
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content

    return respuesta_completa

def main():
    #INCOVANDO FUNCIONES
    modelo = configurar_pagina()
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()
    area_chat()
    mensaje = st.chat_input("Escribi un mensaje:")

    #Verificar si el mensaje tiene contenido
    if mensaje:
        actualizar_historial("user", mensaje, "🕵️‍♂️") #Muestra mensaje del usuario
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje) #Obtiene respuesta
        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "👨‍💻")
                st.rerun()

if __name__ == "__main__":
    main()