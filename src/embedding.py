# This script store the documents into Elasticsearch
# It performs the following steps:
# - read the data/talk*.txt file
# - convert the text into embedding
# - store the embedding and the content in Elasticsearch

import os
import ollama
from pathlib import Path
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

base_path = Path(__file__).parent.parent.resolve()
folder_path = base_path / 'data'

# Create the index in Elasticsearch with dense_vector type

# Read the Elasticsearch configuration file
dotenv_path = Path(base_path / "elastic-start-local/.env")
if not dotenv_path.exists():
    print("Elasticsearch is not installed, please run the following command:")
    print("curl -fsSL https://elastic.co/start-local | sh")
    exit(1)
    
load_dotenv(dotenv_path=dotenv_path)
es = Elasticsearch(
    os.getenv('ES_LOCAL_URL'),
    api_key = os.getenv('ES_LOCAL_API_KEY')
)

index_name = "cloudconf_talks"
# Create the mapping
response = es.indices.create(
    index=index_name,
    mappings={
        "properties": {
            "my_vector": {
                "type": "dense_vector",
                "dims": 3072
            },
            "my_text" : {
                "type" : "text"
            },
            "file" : {
                "type" : "keyword"
            }
        }
    }   
)
print(response)

# Load the txt files in Elasticsearch using Ollama embeddings
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(folder_path, filename)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()


        # convert the content into embedding
        response = ollama.embeddings(model="llama3.2:3b", prompt=content)
        embedding = response["embedding"]
        
        # store the embedding in Elasticsearch
        response = es.index(
            index=index_name,
            document={
                "my_vector" : embedding,
                "my_text" : content,
                "file" : file_path
            }
        )
        print(response)