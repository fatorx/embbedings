from transformers import pipeline

# Choose your desired task and model
classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Get predictions
result = classifier("Oh no, ")
print(result)
