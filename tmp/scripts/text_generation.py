from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")

prompt = "As a English teacher, create a fun sentence with the weather and the name of the city. For example: with Cold and Curitiba, the sentence would be the following: Cold and Curitiba go together, but few people like this combination."
result = generator(prompt, max_length=200, truncation=False)
print(result[0]["generated_text"])
