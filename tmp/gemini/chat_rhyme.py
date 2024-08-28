import time
import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
import base64

os.environ["GOOGLE_API_KEY"] = os.environ.get("GEMINI_API_KEY")
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0
)

SYSTEM_INSTRUCTIONS = "Você é um especialista em textos literário e rimas. Com uma palavra fornecidade pelo usuário, construa duas frases com rimas para a palavra."

def chat_simulation():
    print("Bem-vindo a fabrica de Rimas! Para sair, digite 'exit'.")
    while True:
        user_input = input("> ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        else:
            messages = [
                ("system", SYSTEM_INSTRUCTIONS),
                ("human", user_input)
            ]

            ai_msg = llm.invoke(messages)
            print(ai_msg.content)
            


if __name__ == "__main__":
    chat_simulation()