import os

import google.generativeai as genai

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-flash')

code_single = """
    class Start:
    def __init__(self, message: str):
        self.message = message

    async def get_message(self) -> dict:
        content = "Go to kernel."
        if self.message == 'Where?':
            content = "Go to root."

        data = {
            "content": content,
        }

        return data
"""

result = genai.embed_content(
        model="models/text-embedding-004",
        content=code_single,
        task_type="retrieval_document",
        title="Embedding of single string")

print(str(result['embedding']))