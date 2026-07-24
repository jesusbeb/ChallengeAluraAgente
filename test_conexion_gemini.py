from langchain_google_genai import ChatGoogleGenerativeAI
from my_keys import GEMINI_API_KEY
from my_models import GEMINI_FLASH

llm = ChatGoogleGenerativeAI(
    model=GEMINI_FLASH,
    google_api_key=GEMINI_API_KEY,
    temperature=0.2
)

respuesta = llm.invoke("Responde únicamente: conexión exitosa")

print(respuesta.content)