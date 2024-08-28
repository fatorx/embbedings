import base64
import os
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting, FinishReason
import vertexai.preview.generative_models as generative_models


def generate():
    api_key = os.environ.get("GEMINI_API_KEY")

    vertexai.init(project="games-342612", location="us-central1", api_key=api_key)
    model = GenerativeModel(
        "gemini-1.5-flash-001",
    )
    responses = model.generate_content(
        [video1, text1],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )

    for response in responses:
        print(response.text, end="")


video1 = Part.from_uri(
    mime_type="video/mp4",
    uri="gs://cloud-samples-data/generative-ai/video/pixel8.mp4")
text1 = """Look through each frame in the video carefully and answer the question.
Only base your answers strictly on what information is available in the video attached.
Do not make up any information that is not part of the video and do not be too verbose.

Questions:
- When does a red lantern first appear and what is written in the lantern? Provide a timestamp.
- What language is the person speaking and what does the person say at that time?"""

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
]

generate()
