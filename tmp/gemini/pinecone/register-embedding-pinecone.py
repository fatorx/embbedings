import os

from pinecone import Pinecone
import google.generativeai as genai

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

pc = Pinecone(api_key=PINECONE_API_KEY)

code_single = """
from pydantic import BaseModel, field_validator


class ModelResponseSerializer(BaseModel):
    input: str
    output: str
    uuid: str
    
    MESSAGE="Input text cannot be empty"

    @field_validator("input")
    @classmethod
    def input_not_empty(cls, value):
        if not value.strip():
            raise ValueError(self.MESSAGE)
        return value

    @field_validator("output")
    @classmethod
    def output_not_empty(cls, value):
        if not value.strip():
            raise ValueError(self.MESSAGE)
        return value

"""

index_name = "code-start"
index = pc.Index(index_name)

file_name="response_model.py" # in Python, look at files
path_file="app/schemas/response_model.py"

try:
    result = genai.embed_content(
            model="models/text-embedding-004",
            content=code_single,
            task_type="retrieval_document",
            title=file_name)

    insert_index = "2"
    index.upsert(
         vectors=[
             {
                 "id": "app.schemas." + file_name + insert_index,
                 "values": result['embedding'],
                 "metadata": {"path": path_file, "class": file_name}
             }
         ],
    )

except Exception as e:
    print(e)