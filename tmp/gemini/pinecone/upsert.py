import os
from pinecone import Pinecone, ServilessSpec

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')

pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "pinecone-index"

def get_names_indexes(conn):
    data = conn.list_indexes()
    return [index['name'] for index in data.get('indexes')]

if index_name not in get_names_indexes(pc):
    pc.create_index(
        name=index_name,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

