import os
import subprocess
import sys

import google.generativeai as genai
from google.generativeai import GenerationConfig


class CodeGenerator:
    def __init__(self, api_key=None):
        """
        Inicializa a classe GeminiTranslator.

        Args:
            api_key (str, optional): A chave de API do Gemini.
                                     Se não for fornecida, será obtida da variável de ambiente GEMINI_API_KEY.
        """

        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        genai.configure(api_key=self.api_key)

        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        gen_config = GenerationConfig(**self.generation_config)
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=gen_config,
            system_instruction="""
                    Generate well-structured Python code adhering to PEP 8 style guidelines. 
                    Include clear docstrings and inline comments to explain the code's purpose and logic.
                    The output must be only the code and if the solution requires multiple files, separate them with '####'.
                """
        )

        self.chat_session = self.model.start_chat()

    def get_code(self, message):
        response = self.chat_session.send_message(message)
        return response.text


def create_file(file_name, content=""):
    """Creates a file with the given name and content in the current directory."""

    try:
        with open(file_name, "w") as f:
            f.write(content)
        print(f"File '{file_name}' created successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


def run_and_check_python_file(file_path):
    """Runs a Python file and checks if it executed successfully."""

    try:
        # Use subprocess to run the Python file
        result = subprocess.run([sys.executable, file_path], capture_output=True, text=True)

        # Check the return code (0 indicates success)
        if result.returncode == 0:
            print(f"File '{file_path}' ran successfully.")
            # Optionally, print the output
            print("Output:")
            print(result.stdout)
        else:
            print(f"File '{file_path}' encountered an error.")
            print("Error message:")
            print(result.stderr)

    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def remove_code_blocks(text):
    """Removes `python and ` from a string."""

    # Remove "```python"
    cleaned_text = text.replace("```python", "")

    # Remove "```" (even if not followed by "python")
    cleaned_text = cleaned_text.replace("```", "")

    return cleaned_text


if len(sys.argv) > 1:
    question = sys.argv[1]

    generator = CodeGenerator()
    code = generator.get_code(question)
    file = 'test.py'
    create_file(file, remove_code_blocks(code))
    run_and_check_python_file(file)
