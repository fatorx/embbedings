import tiktoken

tokenizer = tiktoken.get_encoding("cl100k_base")


# create the length function
def get_tokens(text):
    tokens = tokenizer.encode(
        text,
        disallowed_special=()
    )
    return tokens

items = get_tokens("hello I am a chunk of text and using the tiktoken_len function "
             "we can find the length of this chunk of text in tokens")

print(items)