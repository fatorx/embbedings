import os
import weaviate
import warnings
import google.generativeai as genai

warnings.filterwarnings("ignore", category=DeprecationWarning, module="weaviate")

# Best practice: store your credentials in environment variables
wcd_url = os.environ.get("WCD_DEMO_URL")
wcd_api_key = os.environ.get("WCD_DEMO_RO_KEY")
provider_api_key = os.environ.get("GEMINI_API_KEY")

auth_config = weaviate.auth.AuthApiKey(api_key=wcd_api_key)

client = weaviate.Client(
    url=wcd_url,  # URL of your Weaviate instance
    auth_client_secret=auth_config,
    timeout_config=(5, 15),  # (Optional) Set connection timeout & read timeout time in seconds
    additional_headers={"X-Google-Api-Key": provider_api_key}
)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-flash')

result = genai.embed_content(
    model="models/text-embedding-004",
    content="Hello world",
    task_type="retrieval_document",
    title="Embedding of single string")

print(str(result['embedding']))

# client = weaviate.connect_to_weaviate_cloud(
#     cluster_url=wcd_url,                                    # Replace with your Weaviate Cloud URL
#     auth_credentials=wvc.init.Auth.api_key(wcd_api_key),    # Replace with your Weaviate Cloud key
#     headers={"X-Google-Api-Key": provider_api_key}            # Replace with appropriate header key/value pair for the required API
# )

#assert client.is_ready()

# finally:
#     client.close()  # Close client gracefully