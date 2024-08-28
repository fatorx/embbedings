import os
import openai
from pinecone import Pinecone as PineconeClient, ServerlessSpec
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import MarkdownHeaderTextSplitter
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate

# Carregar variáveis de ambiente
load_dotenv(dotenv_path='.env')
openai.api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_env = os.getenv("PINECONE_ENV")

# Inicializar o Pinecone
pc = PineconeClient(api_key=pinecone_api_key, environment=pinecone_env)
index_name = "document-embeddings"

# Verificar se o índice já existe, caso contrário, criar um novo
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  # Dimensão dos embeddings do modelo OpenAI
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

# Conectar ao índice do Pinecone
index = pc.Index(index_name)

# Inicializar o modelo LLM da OpenAI
llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")
embeddings = OpenAIEmbeddings()

# Definir o template de prompt
prompt = ChatPromptTemplate.from_template("""
Responda a pergunta com base no contexto abaixo. Seja breve e objetivo.
{context}
Pergunta: {query}
""")

# Carregar o conteúdo do arquivo
file_path = '/home/jack/Downloads/ingresse-data/app/test.py'
with open(file_path, 'r') as file:
    markdown_document = file.read()

# Dividir o texto com base nos cabeçalhos Markdown
headers_to_split_on = [("##", "Header 2")]
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on, strip_headers=False)
md_header_splits = markdown_splitter.split_text(markdown_document)

# Fazer o embed e subir para o Pinecone
for i, content in enumerate(md_header_splits):
    content_str = str(content)  # Garantir que o conteúdo seja uma string
    embed = embeddings.embed_query(content_str)
    metadata = {"text": content_str}
    index.upsert(vectors=[(f"{file_path}_{i}", embed, metadata)])  # Corrigido para usar `vectors`

# Realizar uma busca de exemplo no Pinecone
query = "Analise o conteudo e traga uma resposta?"
query_embedding = embeddings.embed_query(query)
search_results = index.query(vector=query_embedding, top_k=5, include_metadata=True)  # Usando argumentos nomeados

# Extrair o contexto dos documentos encontrados
context = "\n".join([match['metadata']['text'] for match in search_results['matches']])

# Gerar o valor do prompt
prompt_value = prompt.format_prompt(context=context, query=query)

# Gerar a resposta usando o LLM
response = llm.invoke(prompt_value.to_messages())

# Exibir a resposta
print(response.content)
