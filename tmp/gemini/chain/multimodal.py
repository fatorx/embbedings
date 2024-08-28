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

def encode_image(path_image):
    with open(path_image, 'rb') as img:
        return base64.b64encode(img.read()).decode('utf-8')

image_data = encode_image('image01.jpg')

message = HumanMessage(
    content=[
        {"type": "text", "text": "O que há nesta imagem?"},
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpge;base64,{image_data}"},
        }
    ]
)

ai_msg = llm.invoke([message])
print(ai_msg.content)