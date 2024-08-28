import google.generativeai as genai
import os


genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-flash')

result = genai.embed_content(
    model="models/text-embedding-004",
    content="Hello world",
    task_type="retrieval_document",
    title="Embedding of single string")

# 1 input > 1 vector output
print(str(result['embedding']))