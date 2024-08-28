import getpass
import os
from langchain_google_genai import ChatGoogleGenerativeAI


os.environ["GOOGLE_API_KEY"] = os.environ.get("GEMINI_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)

messages = [
    ("system", "Você é um assistente que traduz do inglês para o espanhol. Traduza o seguinte."),
    ("human", "I love programming")
]

ai_msg = llm.invoke(messages)
print(ai_msg.content)