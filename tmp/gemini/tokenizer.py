import ast
import subprocess
import os
import google.generativeai as genai
import hashlib
from helpers import get_git_commits
import sqlite3

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL = 'gemini-1.5-flash'

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL)

def generate_embeddings(content):

    result = genai.embed_content(
        model="models/text-embedding-004",
        content=str(content),
        task_type="retrieval_document",
        title="file")

    print(result)

def tokenize_code(code_string):
    tree = ast.parse(code_string)
    tokens = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            tokens.append('def')
            tokens.append(node.name)
            for arg in node.args.args:
                tokens.append(arg.arg)
        elif isinstance(node, ast.Name):
            tokens.append(node.id)
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            tokens.append('STRING')
        elif isinstance(node, ast.Constant) and isinstance(node.value, (int, float, complex)):
            tokens.append('NUMBER')
        elif isinstance(node, ast.keyword):
            tokens.append(node.arg)
        elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            # Handle string concatenation
            left_tokens = tokenize_code(ast.unparse(node.left))
            right_tokens = tokenize_code(ast.unparse(node.right))
            # If both sides are strings, merge them into one
            if left_tokens[-1] == 'STRING' and right_tokens[0] == 'STRING':
                tokens.extend(left_tokens[:-1])
                tokens.append('STRING')
                tokens.extend(right_tokens[1:])
            else:
                tokens.extend(left_tokens)
                tokens.extend(right_tokens)
        # Add more node types as needed

    return tokens

def read_file(file_path, encoding="utf-8"):
  """
  Reads the contents of a file and returns them as a string.

  Args:
      file_path (str): The path to the file to be read.
      encoding (str, optional): The encoding of the file (defaults to 'utf-8').

  Returns:
      str or None: The contents of the file as a string, or None if an error occurs.
  """

  try:
      with open(file_path, 'r', encoding=encoding) as file:
          print('read', file_path)
          contents = file.read()

      return contents

  except FileNotFoundError:
      print(f"Error: File not found at path '{file_path}'")
      return None

  except PermissionError:
      print(f"Error: Permission denied to read file '{file_path}'")
      return None

  except UnicodeDecodeError:
      print(f"Error: Unable to decode file '{file_path}' with encoding '{encoding}'. Try a different encoding.")
      return None

  except Exception as e:
      print(f"An unexpected error occurred while reading '{file_path}': {e}")
      return None

file_path_code = './code_start.py'
code = read_file(file_path_code)

tokens_list = tokenize_code(code)
#print(tokens_list)
print(generate_embeddings(tokens_list))