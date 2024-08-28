import subprocess
import os
from pinecone import Pinecone, ServerlessSpec
import google.generativeai as genai
import hashlib
from helpers import get_git_commits
import sqlite3

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL = 'gemini-1.5-flash'

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL)
pc = Pinecone(api_key=PINECONE_API_KEY)

# question = "What are the services files?"
question = "How to filter input in this application?"
# question = "What is the latest version of input filter?"
#question = "I would like to add a new endpoint"
#question = "Would "
# question = "I would like to add a new configuration environment to application, ignore *.ini files"

result = genai.embed_content(
            model="models/text-embedding-004",
            content=question,
            task_type="retrieval_document",
            title="A search")

# Mock vectorized search query (vectorize with LLM of choice)
query_embedding = result['embedding'] # len(query) = 1536, same as the indexed vectors

index_name = "text-2-query"
index = pc.Index(index_name)

# Send query with (optional) filter to index and get back 1 result (top_k=1)
result_search  = index.query(
    vector=query_embedding,
    include_values=True,
    include_metadata=True,
    top_k=10
)

def create_file(file_name, content=""):
    """Creates a file with the given name and content in the current directory."""

    try:
        with open(file_name, "w") as f:
            f.write(content)
        print(f"File '{file_name}' created successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

create_file('result.txt', str(result_search))
#print(result_search)

for rs in result_search['matches']:
    print(rs.get('id'))
    print(rs.get('metadata'))
