from langchain.tools import tool
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from my_keys import GEMINI_API_KEY

# Este segundo archivo es el puente entre el "cerebro" y la "boca" del agente (modelo Gemini)
# Se conecta a la carpeta donde se creo la BD vectorial. Cuando el agente use
# esta herramienta, convertira la pregunta del usuario en numeros y buscara los 3 fragmentos (k=3)
# que matematicamente se parezcan mas a la pregunta.

# 1. Configurar los embeddings (debe ser exactamente el mismo modelo que usamos para crear la BD)
# Se crea el objeto que convierte texto (pregunta del usuario) en vectores numéricos para 
# poder buscar similitud semántica en la base de datos vectorial.
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=GEMINI_API_KEY
)

# 2. Conectar a la base de datos local existente para dejarla lista al agente
# Chroma es una BD vectorial que almacena y busca documentos por significado, no solo por
# palabras exactas. Tiene guardados fragmentos de texto como vectores numericos.
print("Conectando a la base de datos vectorial...")
vectorstore = Chroma(
    persist_directory="./bd_vectorial",
    embedding_function=embeddings
)

# 3. Definimos la herramienta y la marcamos con @tool para indicar que podra ser usada por el agente.
# Recibe un parametro llamado pregunta de tipo String y devuelve un String  -> str
# La descripcion de @tool es lo que Gemini lee para decidir si debe usar esta herramienta o no.
@tool
def consultar_documentos_empresa(pregunta: str) -> str:
    """
    Usa esta herramienta SIEMPRE que necesites responder preguntas a clientes de la empresa BimBam Buy.
    Que es un e-commerce multiplataforma enfocado en la experiencia de compra digital ágil y segura. 
    Se destaca por un modelo de negocio orientado al cliente, con políticas robustas de reembolsos y devoluciones, 
    un programa de afiliados dinámico y una infraestructura logística optimizada para garantizar 
    entregas rápidas, garantia de productos, metodos de pago y soporte constante al usuário final.
    """
    # Buscar los fragmentos más relevantes en la base de datos (k=3 significa traer los 3 mejores fragmentos)
    fragmentos_encontrados = vectorstore.similarity_search(pregunta, k=3)
    
    # Unir los fragmentos encontrados en un solo texto
    textos_extraidos = [doc.page_content for doc in fragmentos_encontrados]
    respuesta_contexto = "\n\n---\n\n".join(textos_extraidos)
    
    return respuesta_contexto