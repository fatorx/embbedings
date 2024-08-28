import os

files_content = []

def calculate_total_bytes(directory):
    total_bytes = 0
    print(directory)
    for root, dirs, files in os.walk(directory):

        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            total_bytes += os.path.getsize(file_path)
            print(f"File: {file_path}, Size: {file_size} bytes")
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                files_content.append({
                    "file_path" : file_path,
                    "content" : content,
                })
    
    return total_bytes

def bytes_to_megabytes(bytes_calc):
    return bytes_calc / (1024 * 1024)

if __name__ == "__main__":
    project_directory = "/home/fabiosmendes/projects/python/embeddings/app"  # Altere para o caminho do seu projeto FastAPI
    total_bytes_start = calculate_total_bytes(project_directory)
    total_megabytes = bytes_to_megabytes(total_bytes_start)
    print(f"Total de bytes no projeto: {total_bytes_start} bytes")
    print(f"Total de megabytes no projeto: {total_megabytes:.2f} MB")

    print(files_content)