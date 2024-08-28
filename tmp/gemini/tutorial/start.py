import os

import google.generativeai as genai

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-flash')

response = model.generate_content("Write a story about an AI and a boy in 100 characters.")

file_name = 'content/response.txt'
with open(file_name, "a+") as f:
    #f.write(str(response))
    f.write(response.text)

    # \"You're my friend,\" the boy said. The AI blinked,
    # \"I am programmed to assist, not befriend.\"
    # The boy smiled, \"Then assist me in being happy.\" \n"

    # "I'm not a machine,\" said the boy. The AI blinked, \"Then why do you obey me?\" \n"

    # "He's just a program,\" she scoffed. He blinked, his digital eyes reflecting her tears.
    # \"No,\" he whispered, \"I'm your friend.\"