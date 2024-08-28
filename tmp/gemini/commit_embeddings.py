import subprocess
import os
from pinecone import Pinecone, ServerlessSpec
import google.generativeai as genai
import hashlib
from helpers import get_git_commits
import sqlite3

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL = 'gemini-1.5-flash'

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL)
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "text-2-query"

def get_names_indexes(conn):
    data = conn.list_indexes()
    return [index['name'] for index in data.get('indexes')]

if index_name not in get_names_indexes(pc):
    pc.create_index(
        name=index_name,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

index = pc.Index(index_name)
list_files = []


def list_directories(folder_path):
    try:
        # List all items in the folder
        items = os.listdir(folder_path)

        # Filter the list to include only directories
        directories = [item for item in items if os.path.isdir(os.path.join(folder_path, item))]

        return directories

    except FileNotFoundError:
        print(f"The folder '{folder_path}' was not found.")
        return None
    except PermissionError:
        print(f"Permission denied to access the folder '{folder_path}'.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def load_gitignore(path):
    gitignore_path = os.path.join(path, '.gitignore')
    ignores = set()

    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    ignores.add(path + '/' + line)

    return ignores

def read_file(file_path, encoding='utf-8'):
  """Reads the contents of a file and returns them as a string.

  Args:
      file_path: The path to the file to be read.
      encoding: The encoding of the file (defaults to 'utf-8').

  Returns:
      The contents of the file as a string, or None if an error occurs.
  """

  try:
      with open(file_path, 'r', encoding=encoding) as file:
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

def list_dir(path, ignores, level=0):
    try:
        items = os.listdir(path)

    except FileNotFoundError:
        print(f"The directory '{path}' was not found.")
        return
    except PermissionError:
        print(f"Permission denied to access directory '{path}'.")
        return

    items.sort()

    for item in items:
        if item in ['.gitignore', 'poetry.lock', 'storage', 'build', '.git', 'docs', 'docker-compose.yaml', 'dev.Dockerfile', 'commit.sh']:
            continue

        path_complete = os.path.join(path, item)

        if item in ignores or any(os.path.join(root, item) in ignores for root, _, _ in os.walk(path)):
            continue

        if os.path.isdir(path_complete):
            list_dir(path_complete, ignores, level + 1)
            continue

        parts = path_complete.split("/storage/")
        path_commit = parts[1]

        file_content = "```python\n"
        file_content += read_file(path_complete)
        file_content += "```"

        list_files.append({
            "path": path_commit,
            "content": file_content
        })

def string_to_hash(input_string):
    # Create a SHA-256 hash object
    hash_object = hashlib.sha256()

    # Encode the string to bytes and update the hash object
    hash_object.update(input_string.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    hex_dig = hash_object.hexdigest()

    return hex_dig

def generate_embeddings(project, commit_hash, storage_directory):
    """Executes the specified shell commands."""
    commit_path = f"{storage_directory}/{commit_hash}"

    ignores = load_gitignore(commit_path)
    list_dir(commit_path, ignores)

    for file_data in list_files:
        path_file = file_data.get('path')
        hash_file = string_to_hash(path_file)
        content = file_data.get('content')

        result = genai.embed_content(
            model="models/text-embedding-004",
            content=content,
            task_type="retrieval_document",
            title=path_file)

        print(path_file)
        print(result)
        break
        # index.upsert(
        #     vectors=[
        #         {
        #             "id": hash_file,
        #             "values": result['embedding'],
        #             "metadata": {"path": path_file}
        #         }
        #     ],
        # )

if __name__ == "__main__":
    base_dir = "/api/tmp/gemini"
    project = 'text-2-query'
    destination_base_folder = base_dir + '/storage'

    storage_directory = f"{destination_base_folder}/{project}"
    commits = list_directories(storage_directory)

    for commit_hash in commits:
        generate_embeddings(project, commit_hash, storage_directory)
        break



