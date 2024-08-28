import json
import os

import requests
import weaviate
import warnings
import google.generativeai as genai

from weaviate.classes.config import Configure, Property, DataType
import weaviate.classes as wvc
from weaviate.util import get_vector  # Helper to format vectors

warnings.filterwarnings("ignore", category=DeprecationWarning, module="weaviate")

# Best practice: store your credentials in environment variables
wcd_url = os.environ.get("WCD_DEMO_URL")
wcd_api_key = os.environ.get("WCD_DEMO_RO_KEY")
provider_api_key = os.environ.get("GEMINI_API_KEY")

auth_config = weaviate.auth.AuthApiKey(api_key=wcd_api_key)

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=wcd_url,                                    # Replace with your Weaviate Cloud URL
    auth_credentials=wvc.init.Auth.api_key(wcd_api_key),    # Replace with your Weaviate Cloud key
    headers={"X-Google-Studio-Api-Key": provider_api_key}            # Replace with appropriate header key/value pair for the required API
)

try:
    collection_name = "Question"
    questions = client.collections.get("Question")

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

    response = questions.query.near_text(
        query="biology",
        limit=2
    )

    print(response.objects[0].properties)  # Inspect the first object

finally:
    client.close()  # Close client gracefully







