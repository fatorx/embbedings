import os
import time
import streamlit as st
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from openai_utils import OpenAIUtils
import hashlib
import zipfile

# Carregar variáveis de ambiente
load_dotenv()
openai_utils = OpenAIUtils()

# Inicializar o estado da sessão se não estiver inicializado
if 'processed_files' not in st.session_state:
    st.session_state['processed_files'] = set()

if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'Página Principal'

# Configurar a navegação usando botões
st.sidebar.title("Navegação")
st.markdown(
    """
    <style>
    .stButton > button {
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #ffff; /* Cor de fundo no hover */
        color: white; /* Cor do texto no hover */
        border-color: #ffff; /* Cor da borda no hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)
if st.sidebar.button("Página Principal"):
    st.session_state['current_page'] = 'Página Principal'
if st.sidebar.button("Upload de Projeto e Q&A"):
    st.session_state['current_page'] = 'Upload de Projeto e Q&A'
if st.sidebar.button("Chat"):
    st.session_state['current_page'] = 'Chat'

# Página Principal
if st.session_state['current_page'] == "Página Principal":
    st.title("Bem-vindo ao Sistema de Processamento de Projetos")
    st.write("""
    Este sistema permite que você faça upload de projetos, faça perguntas sobre eles e interaja com um chat inteligente.
    Use os botões na barra lateral para navegar entre as páginas:

    - **Upload de Projeto e Q&A:** Envie arquivos de projetos, que serão processados e armazenados no Pinecone, permitindo perguntas sobre o conteúdo.
    - **Chat:** Interaja com um chat que responde suas perguntas e auxilia com base nos projetos carregados.
    """)

# Página de Upload de Projeto e Q&A
elif st.session_state['current_page'] == "Upload de Projeto e Q&A":
    from pinecone_utils import PineconeUtils  # Importar somente se estiver nesta página

    # Inicializar Pinecone na página de upload
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pinecone_env = os.getenv("PINECONE_ENV")
    pinecone_utils = PineconeUtils(api_key=pinecone_api_key, environment=pinecone_env, index_name="document-embeddings")

    st.title("Upload de Projeto e Q&A")

    # Upload de arquivo ZIP
    uploaded_file = st.file_uploader("Faça upload de um arquivo ZIP contendo seu projeto", type=["zip"])

    if uploaded_file:
        start_time = time.time()
        zip_file_name = os.path.splitext(uploaded_file.name)[0]  # Nome do projeto com base no nome do arquivo ZIP
        st.write(f"Iniciando processamento do ZIP '{zip_file_name}'...")
        st.markdown(f"<script>console.log('Iniciando processamento do ZIP {zip_file_name}...')</script>",
                    unsafe_allow_html=True)

        # Salvar o arquivo zip temporariamente
        with open('/tmp/uploaded.zip', 'wb') as temp_zip:
            temp_zip.write(uploaded_file.read())

        with zipfile.ZipFile('/tmp/uploaded.zip', 'r') as zip_ref:
            zip_ref.extractall('/tmp/unzipped')

        st.success("Arquivo ZIP descompactado com sucesso!")
        st.write("Iniciando o processamento dos arquivos...")
        st.markdown(f"<script>console.log('Arquivo ZIP descompactado com sucesso!')</script>", unsafe_allow_html=True)

        # Extensões permitidas
        allowed_extensions = {".py", ".md", ".txt", ".yaml", ".yml", "Dockerfile"}

        # Lista para armazenar as mensagens de sucesso
        success_messages = []

        # Inicializar o text splitter
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

        # Contagem total de arquivos permitidos
        total_files = sum(1 for root, _, files in os.walk('/tmp/unzipped')
                          for file_name in files if
                          os.path.splitext(file_name)[1] in allowed_extensions or file_name.endswith('Dockerfile'))
        progress_bar = st.progress(0)  # Barra de progresso
        file_count = 0  # Contador de arquivos processados

        # Processar arquivos extraídos
        for root, _, files in os.walk('/tmp/unzipped'):
            for file_name in files:
                file_path = os.path.join(root, file_name)

                # Obter a extensão do arquivo
                file_extension = os.path.splitext(file_name)[1]

                # Verificar se o arquivo tem uma extensão permitida ou é um Dockerfile (que pode não ter extensão)
                if file_extension not in allowed_extensions and not file_name.endswith('Dockerfile'):
                    continue

                # Atualizar a barra de progresso com a porcentagem correta
                file_count += 1
                progress_percentage = file_count / total_files
                progress_bar.progress(progress_percentage)

                # Exibir a mensagem de processamento em um box azul
                st.info(f"Processando arquivo: {file_name}... ({int(progress_percentage * 100)}%)")

                action_start_time = time.time()

                # Tentar ler o conteúdo do arquivo
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                except UnicodeDecodeError:
                    st.write(f"Falha ao ler o arquivo {file_name} devido a um erro de decodificação.")
                    continue

                # Calcular o hash do conteúdo
                content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
                time.sleep(1)

                # Fazer o upload do conteúdo para o Pinecone, incluindo o nome do projeto nos metadados
                metadata = {
                    "file_name": file_name,
                    "project_name": zip_file_name,  # Adicionando o nome do projeto aos metadados
                    "content_hash": content_hash,
                    "text_snippet": content[:1000]  # Usando apenas os primeiros 1000 caracteres como exemplo
                }
                pinecone_utils.upsert_document([content], file_name, content_hash, metadata)
                action_end_time = time.time()
                elapsed_time = action_end_time - action_start_time

                success_messages.append(
                    f"Arquivo {file_name} carregado e embeddado no Pinecone com sucesso! (Tempo: {elapsed_time:.2f} segundos)")
                st.session_state['processed_files'].add(content_hash)

        # Exibir as mensagens de sucesso
        for message in success_messages:
            st.success(message)

        st.write("Processamento concluído.")
        st.write(f"Tempo total: {time.time() - start_time:.2f} segundos")

        # Fazer uma pergunta ao documento
        query = st.text_input("Faça uma pergunta ao documento:")

        if query:
            search_results = pinecone_utils.query_document(query)
            context = "\n".join([match['metadata']['text_snippet'] for match in search_results['matches']])

            # Gerar a resposta usando OpenAI
            response = openai_utils.generate_response(context, query)
            st.subheader("Resposta")
            st.write(response)

# Página de Chat
elif st.session_state['current_page'] == "Chat":
    st.title("Chat")
    st.write("Bem-vindo ao chat inteligente! Faça suas perguntas abaixo:")

    # Fazer uma pergunta ao chat
    chat_query = st.text_input("Digite sua pergunta:")

    if chat_query:
        # Inicializar Pinecone para consulta no chat
        from pinecone_utils import PineconeUtils
        pinecone_api_key = os.getenv("PINECONE_API_KEY")
        pinecone_env = os.getenv("PINECONE_ENV")
        pinecone_utils = PineconeUtils(api_key=pinecone_api_key, environment=pinecone_env, index_name="document-embeddings")

        search_results = pinecone_utils.query_document(chat_query)
        context = "\n".join([match['metadata']['text_snippet'] for match in search_results['matches']])

        # Gerar a resposta usando OpenAI
        chat_response = openai_utils.generate_response(context, chat_query)
        st.subheader("Resposta")
        st.write(chat_response)
