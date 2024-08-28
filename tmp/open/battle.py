from openai import OpenAI
import os

OPENAI_API_KEY= os.environ.get("OPEN_API_KEY") # OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Write a rap battle between Alan Turing and Yann LeCun."
                }
            ]
        }
    ],
    temperature=0.8,
    max_tokens=512,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    response_format={
        "type": "text"
    }
)

print(response.choices[0].message.content)