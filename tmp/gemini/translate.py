"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import os

import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction="Se a frase ou pergunta informada pelo usuário for em português, traduza para o Inglês",
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "Quais são os produtos mais vendidos?\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "What are the best-selling products? \n",
      ],
    },
  ]
)

response = chat_session.send_message("Quais são os principais fornecedores?")

print(response.text)
