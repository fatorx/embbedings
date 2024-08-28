import google.generativeai as genai
import os
from pinecone import Pinecone, ServerlessSpec

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL = 'gemini-1.5-flash'

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL)
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "text-2-query"

def get_names_indexes(conn):
    data = conn.list_indexes()
    # return conn.list_indexes().names()
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

index = pc.Index(index_name)