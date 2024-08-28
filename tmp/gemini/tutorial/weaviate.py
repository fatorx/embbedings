import json
import os

import requests
import weaviate
import warnings
import google.generativeai as genai

from weaviate.classes.config import Configure, Property, DataType
import weaviate.classes as wvc
from weaviate.util import get_vector  # Helper to format vectors

# Best practice: store your credentials in environment variables
wcd_url = os.environ.get("WCD_DEMO_URL")
wcd_api_key = os.environ.get("WCD_DEMO_RO_KEY")
provider_api_key = os.environ.get("GEMINI_API_KEY")

auth_config = weaviate.auth.AuthApiKey(api_key=wcd_api_key)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=wcd_url,                                    # Replace with your Weaviate Cloud URL
    auth_credentials=wvc.init.Auth.api_key(wcd_api_key),    # Replace with your Weaviate Cloud key
    headers={"X-Google-Studio-Api-Key": provider_api_key}            # Replace with appropriate header key/value pair for the required API
)

try:


    def get_embed(text):
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_document",
            title="Embedding of single string")

        return str(result['embedding'])


    if client.collections.exists("Question") is False:
        client.collections.create(
            name="Question",
            vectorizer_config=Configure.Vectorizer.none(),  # No built-in vectorization
            properties=[
                Property(name="answer", data_type=DataType.TEXT),
                Property(name="question", data_type=DataType.TEXT),
                Property(name="category", data_type=DataType.TEXT),
            ]
        )


    def add_question(answer, question, category):
        answer_embedding = get_embed(answer)  # Get embedding from Gemini
        body_embedding = get_embed(question)
        category_embedding = get_embed(category)

        questions = client.collections.get("Question")
        # vector_data = get_vector(answer_embedding + body_embedding + category_embedding)
        properties = {
            "answer": d["Answer"],
            "question": d["Question"],
            "category": d["Category"],
        }

        questions.data.create(properties)

    # Example usage
    resp = requests.get('https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json')
    data = json.loads(resp.text)  # Load data

    question_objs = list()
    for i, d in enumerate(data):
        question_objs.append({
            "answer": d["Answer"],
            "question": d["Question"],
            "category": d["Category"],
        })

    questions = client.collections.get("Question")
    questions.data.insert_many(question_objs)

finally:
    client.close()  # Close client gracefully







