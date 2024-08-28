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
  model_name="gemini-1.5-pro-exp-0801",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "Write a function to read a file\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```python\ndef read_file(file_path):\n  \"\"\"Reads a file and returns its contents.\n\n  Args:\n    file_path: The path to the file to read.\n\n  Returns:\n    The contents of the file as a string.\n  \"\"\"\n  with open(file_path, 'r') as f:\n    contents = f.read()\n  return contents\n```",
      ],
    },
    {
      "role": "user",
      "parts": [
        "crie uma função para ler um arquivo xml e converta para json",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```python\nimport xml.etree.ElementTree as ET\nimport json\n\ndef xml_to_json(xml_file):\n  \"\"\"Lê um arquivo XML e o converte para JSON.\n\n  Args:\n    xml_file: Caminho para o arquivo XML.\n\n  Returns:\n    Um dicionário Python representando o conteúdo JSON.\n  \"\"\"\n  tree = ET.parse(xml_file)\n  root = tree.getroot()\n\n  def element_to_dict(element):\n    \"\"\"Converte um elemento XML em um dicionário Python.\"\"\"\n    result = {}\n    for child in element:\n      if child.tag == 'data':\n        result[child.tag] = child.text\n      else:\n        result[child.tag] = element_to_dict(child)\n    return result\n\n  data = element_to_dict(root)\n  return json.dumps(data)\n```",
      ],
    },
  ]
)

response = chat_session.send_message("INSERT_INPUT_HERE")

print(response.text)