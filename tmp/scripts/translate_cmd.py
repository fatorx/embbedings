from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load the T5-base model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("t5-base")


def translate_text(text, source_language, target_language):
    """
    Translates text using the T5-base model.

    Args:
        text: The input text to translate.
        source_language: The language code of the source language (e.g., "en").
        target_language: The language code of the target language (e.g., "fr").

    Returns:
        The translated text.
    """
    # Prepend the task instruction to the input text
    task_prefix = f"translate {source_language} to {target_language}: "
    input_text = task_prefix + text

    # Tokenize the input text
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids

    # Generate the translation
    outputs = model.generate(input_ids, max_length=128)

    # Decode the output tokens and remove the task prefix
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return translated_text


# Example usage
text = "Gostaria de ver as vendas com maior valor desse mês."
source_lang = "pt"
target_lang = "en"

translated_text = translate_text(text, source_lang, target_lang)
print(f"Original: {text}\nTranslated: {translated_text}")
