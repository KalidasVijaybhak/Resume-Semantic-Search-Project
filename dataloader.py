
documents = []
from langchain_community.document_loaders import PyPDFLoader
import os

# dataset_folder_path = '/path/to/your/dataset/folder'
max_files = 100
file_count = 0

for file in os.listdir(dataset_folder_path):
    file_path = os.path.join(dataset_folder_path, file)

    # Check if the file is not empty
    if os.path.getsize(file_path) == 0:
        print(f"Skipping empty file: {file}")
        continue

    loader = PyPDFLoader(file_path)
    try:
        loader = PyPDFLoader(file_path)
        documents.extend(loader.load())
    except :
        print(f"Error loading file {file}")
        continue

    # file_count += 1
    # if file_count >= max_files:
    #     break