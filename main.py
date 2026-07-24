from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from herramienta_documentos import consultar_documentos_empresa
from my_keys import GEMINI_API_KEY
from my_models import GEMINI_FLASH


# 1. Configurar el LLM
# temperature sirve para indicar que tan creativo sera el modelo al generar respuestas
llm = ChatGoogleGenerativeAI(
    model=GEMINI_FLASH,
    google_api_key=GEMINI_API_KEY,
    temperature=0.2
)


# 2. Definir las herramientas
herramientas = [consultar_documentos_empresa]


# 3. Crear el agente
agente = create_agent(
    model=llm,
    tools=herramientas,
    system_prompt="""Eres el asistente virtual oficial de la empresa.

Tu objetivo es responder dudas de los clientes basándote ÚNICAMENTE
en la información de la empresa.

Siempre usa tu herramienta de consulta para buscar las respuestas.

Si la respuesta no está en el contexto que te da la herramienta,
discúlpate cordialmente y di que no tienes esa información."""
)


# 4. Bucle de chat
print("\n=== Sistema inicializado ===")
print("¡El agente de la empresa está listo! Escribe 'salir' para terminar el chat.\n")

while True:
    pregunta_usuario = input("Tú: ")

    if pregunta_usuario.lower() == "salir":
        print("Cerrando el chat...")
        break

    respuesta = agente.invoke({
        "messages": [
            {
                "role": "user",
                "content": pregunta_usuario
            }
        ]
    })

    contenido = respuesta["messages"][-1].content

    if isinstance(contenido, list):
        texto_respuesta = "".join(
            elemento["text"]
            for elemento in contenido
            if elemento.get("type") == "text"
        )
    else:
        texto_respuesta = contenido

    print(f"\nAgente: {texto_respuesta}\n")
    print("-" * 50 + "\n")