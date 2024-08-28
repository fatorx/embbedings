import os

from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI, HarmBlockThreshold,  HarmCategory

import base64

os.environ["GOOGLE_API_KEY"] = os.environ.get("GEMINI_API_KEY")
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    },
    temperature=0
)

question = "Escreva uma piada sobre modelos de linguagem."

for chunk in llm.stream(question):
    print(chunk.content)
    print("---")
