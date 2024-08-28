import os
from pinecone import Pinecone, ServerlessSpec

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")

pc = Pinecone(api_key=PINECONE_API_KEY)

def get_names_indexes(conn):
    data = conn.list_indexes()
    # return conn.list_indexes().names()
    return [index['name'] for index in data.get('indexes')]

list = get_names_indexes(pc)

start_index = "code-start"
if start_index not in list:
    # details = pc.describe_index(start_index)
    # print(details)
    pc.create_index(
        name=start_index,
        dimension=768, # Replace with your model dimensions
        metric="cosine", # Replace with your model metric
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )
else:
    print(list)


