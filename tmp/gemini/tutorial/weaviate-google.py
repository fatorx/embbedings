import json
import os

import google.generativeai as genai
import requests
import weaviate
import weaviate.classes as wvc
from weaviate.classes.config import Configure, Property, DataType


wcd_url = os.environ.get("WCD_DEMO_URL")
wcd_api_key = os.environ.get("WCD_DEMO_RO_KEY")
provider_api_key = os.environ.get("GEMINI_API_KEY")

auth_config = weaviate.auth.AuthApiKey(api_key=wcd_api_key)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=wcd_url,
    auth_credentials=wvc.init.Auth.api_key(wcd_api_key),
    headers={"X-Google-Api-Key": provider_api_key}
)

try:
    collection_name = "Question"

    def get_embed(text):
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_document",
            title="Embedding of single string")

        return str(result['embedding'])


    if client.collections.exists(collection_name) is False:
        print('Create ' + collection_name)
        client.collections.create(
            collection_name,
            vectorizer_config=[
                Configure.NamedVectors.text2vec_palm(
                    project_id="xd123",
                    name="title_vector",
                    source_properties=["title"],
                    # (Optional) To manually set the model ID
                    model_id="text-embedding-004"
                )
            ],
            properties=[
                Property(name="answer", data_type=DataType.TEXT),
                Property(name="question", data_type=DataType.TEXT),
                Property(name="category", data_type=DataType.TEXT),
            ]
        )

    print('Continue')

    resp = requests.get('https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json')
    data = json.loads(resp.text)  # Load data

    question_objs = list()
    for i, d in enumerate(data):
        question_objs.append({
            "answer": d["Answer"],
            "question": d["Question"],
            "category": d["Category"],
        })

    questions = client.collections.get(collection_name)
    print(os.environ.get("GOOGLE_APIKEY"))
    print(questions.data)
    print('')
    questions.data.insert_many(question_objs)

# except Exception as e:
#     print(e.args)
finally:
    client.close()  # Close client gracefully







