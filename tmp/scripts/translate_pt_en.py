from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load the model and tokenizer that have been specifically trained on Portuguese-English translation
tokenizer = AutoTokenizer.from_pretrained("unicamp-dl/translation-pt-en-t5")
model = AutoModelForSeq2SeqLM.from_pretrained("unicamp-dl/translation-pt-en-t5")


def translate_pt_to_en(text):
    input_text = "translate Portuguese to English: " + text
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids

    outputs = model.generate(
        input_ids,
        max_length=128,  # Adjust if your translations tend to be longer
        num_beams=5,  # Beam search for better quality (adjust or remove if you prioritize speed)
        early_stopping=True
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)


# Example usage
text_pt = "What are the most popular products among corporate customers?"

translated_text = translate_pt_to_en(text_pt)
print(f"Portuguese: {text_pt}\nEnglish: {translated_text}")
