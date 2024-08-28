from transformers import pipeline

generator = pipeline("translate", model="google-t5/t5-base")

prompt = "Do like rock and roll music?"
result = generator(prompt, max_length=50, truncation=True)
print(result[0]["generated_text"])

#

from transformers import T5Tokenizer, T5Model

tokenizer = T5Tokenizer.from_pretrained("t5-base")
model = T5Model.from_pretrained("t5-base")

input_ids = tokenizer(
    "Studies have been shown that owning a dog is good for you", return_tensors="pt"
).input_ids  # Batch size 1
decoder_input_ids = tokenizer("Studies show that", return_tensors="pt").input_ids  # Batch size 1

# forward pass
outputs = model(input_ids=input_ids, decoder_input_ids=decoder_input_ids)
last_hidden_states = outputs.last_hidden_state
