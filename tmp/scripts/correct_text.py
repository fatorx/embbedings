import language_tool_python

# Initialize the Portuguese language tool (you can specify a dialect if needed)
tool = language_tool_python.LanguageTool('pt')


def correct_portuguese_text(text):
    """
    Corrects grammatical and spelling errors in Portuguese text.

    Args:
        text: The Portuguese text to correct.

    Returns:
        The corrected text.
    """

    # Check the text for errors
    matches = tool.check(text)

    # Create a corrected text
    corrected_text = language_tool_python.utils.correct(text, matches)

    return corrected_text


# Example usage
text_pt = "Comu que foi as vendas esse mes?"
corrected_text = correct_portuguese_text(text_pt)
print(f"Original: {text_pt}\nCorrected: {corrected_text}")
