import streamlit as st
from pinecone import Pinecone as PineconeClient, ServerlessSpec
from langchain_openai import OpenAIEmbeddings

class PineconeUtils:
    def __init__(self, api_key, environment, index_name):
        self.pc = PineconeClient(api_key=api_key, environment=environment)
        self.index_name = index_name
        self.embeddings = OpenAIEmbeddings()

        # Verificar se o índice já existe antes de tentar criá-lo
        if index_name not in self.pc.list_indexes():
            try:
                self.pc.create_index(
                    name=index_name,
                    dimension=1536,  # Dimensão dos embeddings do modelo OpenAI
                    metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-east-1")
                )
                st.success(f"Índice '{index_name}' criado com sucesso.")
            except Exception as e:
                if "ALREADY_EXISTS" in str(e):
                    pass  # Evitar múltiplas mensagens de sucesso
                else:
                    st.error(f"Erro ao criar o índice Pinecone: {e}")

        # Conectar ao índice existente ou recém-criado
        self.index = self.pc.Index(index_name)

    def upsert_document(self, content_list, file_name, content_hash, metadata):
        for i, content in enumerate(content_list):
            content_str = str(content)
            embed = self.embeddings.embed_query(content_str)
            self.index.upsert(vectors=[(f"{file_name}_{content_hash}_{i}", embed, metadata)])

    def query_document(self, query, top_k=5):
        query_embedding = self.embeddings.embed_query(query)
        return self.index.query(vector=query_embedding, top_k=top_k, include_metadata=True)