import time
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from my_keys import GEMINI_API_KEY 

# Este primer archivo permite darle al agente un "cerebro" o memoria a largo plazo, porque ahora ya
# tiene acceso a los documentos de la empresa

# 1. Cargar los PDFs que estan en la carpeta resources que se encuentra en la raiz del proyecto
print("Cargando documentos (PDF)")
loader = PyPDFDirectoryLoader("resources")
documentos = loader.load()
print(f"Se cargaron {len(documentos)} páginas en total.")

# 2. Fragmentación (Chunking)
print("Dividiendo los documentos en fragmentos...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
fragmentos = text_splitter.split_documents(documentos)
print(f"Se crearon {len(fragmentos)} fragmentos de texto.")

# 3. Creación de Embeddings y almacenamiento por lotes
print("Configurando el modelo de embeddings...")
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001", 
    google_api_key=GEMINI_API_KEY
)

# Inicializamos la base de datos vacía
vectorstore = Chroma(
    persist_directory="./bd_vectorial",
    embedding_function=embeddings
)

# Definimos el tamaño del lote por debajo del límite de 100
# Esto porque Gemini no acepta mas de 100 solicitudes por minuto
tamano_lote = 80 

print("Guardando fragmentos en la base de datos por lotes...")
for i in range(0, len(fragmentos), tamano_lote):
    # Seleccionamos el bloque actual de fragmentos
    lote = fragmentos[i:i + tamano_lote]
    numero_lote = (i // tamano_lote) + 1
    total_lotes = (len(fragmentos) // tamano_lote) + 1
    
    print(f"Procesando lote {numero_lote} de {total_lotes}...")
    vectorstore.add_documents(lote)
    
    # Si aún quedan lotes por procesar, pausamos 60 segundos
    if i + tamano_lote < len(fragmentos):
        print("Esperando 60 segundos para respetar el límite gratuito de Google...")
        time.sleep(60)

# Finalmente ejecutaremos nuestro archivo con: python crear_bd.py
# Se ejecuta una sola vez para crear la BD o se puede volver a ejecutar si se agregara otro documento PDF
print("¡Proceso terminado! La base de datos vectorial se guardó en la carpeta 'bd_vectorial'.")