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

# questions = ["Escreva uma frase sobre vencer na vida com inteligência", "Escreva uma frase sobre vencer na vida com trabalho"]
#
# results = llm.batch(questions)
# answers_content = ""
# for res in results:
#     answers_content = answers_content + res.content + "\n"


messages = [
    ("system", "Você é uma revisar de textos publicitários. Compare as duas frases e crie uma terceira"),
    ("human", "Escreva uma frase sobre vencer na vida com inteligência")
]

ai_msg = llm.invoke(messages)
print(ai_msg.content)


