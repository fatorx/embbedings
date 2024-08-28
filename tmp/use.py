from word2affect_polish.model_script import CustomModel  # importing the custom model class
from transformers import AutoTokenizer

model_directory = "word2affect_english"  # path to the cloned repository

model = CustomModel.from_pretrained(model_directory)
tokenizer = AutoTokenizer.from_pretrained(model_directory)

inputs = tokenizer("This is a test input.", return_tensors="pt")
outputs = model(inputs['input_ids'], inputs['attention_mask'])

# Print out the emotion ratings
for emotion, rating in zip(['Valence', 'Arousal', 'Dominance', 'Age of Acquisition', 'Concreteness'], outputs):
    print(f"{emotion}: {rating.item()}")
