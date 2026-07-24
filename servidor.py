from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from herramienta_documentos import consultar_documentos_empresa
from my_keys import GEMINI_API_KEY
from my_models import GEMINI_FLASH

# Aqui levantamos un servidor web usando FastAPI. Este framework se encarga de recibir las
# preguntas del usuario, pasarlas al agente y devolver la respuesta en pantalla

app = FastAPI()

# Configurar el LLM y el Agente (el mismo de main.py)
llm = ChatGoogleGenerativeAI(
    model=GEMINI_FLASH,
    google_api_key=GEMINI_API_KEY,
    temperature=0.2
)

agente = create_agent(
    model=llm,
    tools=[consultar_documentos_empresa],
    system_prompt="""Eres el asistente virtual oficial de la empresa.
Tu objetivo es responder dudas de los clientes basándote ÚNICAMENTE
en la información de la empresa.
Siempre usa tu herramienta de consulta para buscar las respuestas.
Si la respuesta no está en el contexto que te da la herramienta,
discúlpate cordialmente y di que no tienes esa información."""
)

# Estructura de datos para recibir el mensaje del frontend
class MensajeUsuario(BaseModel.model if hasattr(BaseModel, 'model') else object): # O BaseModel estándar
    pass

class ChatRequest(BaseModel):
    mensaje: str

# Ruta para servir el archivo index.html automáticamente al abrir el navegador
@app.get("/")
def leer_index():
    return FileResponse("index.html")

# Ruta que procesa el chat
@app.post("/chat")
def chatear_con_agente(data: ChatRequest):
    pregunta_usuario = data.mensaje
    
    # Ejecutamos el agente de la misma forma que en el bucle de consola
    respuesta = agente.invoke({
        "messages": [
            {
                "role": "user",
                "content": pregunta_usuario
            }
        ]
    })

    contenido = respuesta["messages"][-1].content

    # Limpiamos el formato de la respuesta si viene en lista
    if isinstance(contenido, list):
        texto_respuesta = "".join(
            elemento["text"]
            for elemento in contenido
            if elemento.get("type") == "text"
        )
    else:
        texto_respuesta = contenido

    return {"respuesta": texto_respuesta}