import getpass
import os
from langchain_google_genai import ChatGoogleGenerativeAI, HarmBlockThreshold,  HarmCategory


os.environ["GOOGLE_API_KEY"] = os.environ.get("GEMINI_API_KEY")
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    },
    temperature=0
)

messages = [
    ("system", "You are a software developer. Explain concepts to others people outside of your field of expertise."),
    ("human", "Explain microservices")
]

ai_msg = llm.invoke(messages)
print(ai_msg.content)