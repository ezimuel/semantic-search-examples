# Semantic search using Elasticsearch

import os
import ollama
from pathlib import Path
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

base_path = Path(__file__).parent.parent.resolve()
folder_path = base_path / 'data'

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
question = "What is semantic search?"

while True:
    user_input = input("Enter a query (or type '\\bye' to quit): ")
    
    # Check if the user typed the stop command
    if user_input == "\\bye":
        print("Exiting...")
        break
    
    response = ollama.embeddings(model="llama3.2:3b", prompt=user_input)
    question_embedding = response["embedding"]

    # Semantic search: retrieval the relevant chunks
    response = es.search(
        index=index_name,
        filter_path="hits.hits",
        knn={
            "field": "my_vector",
            "query_vector": question_embedding,
            "k": 3,
            "num_candidates": 10
        },
        fields=[
            "my_text",
            "file"
        ],
        source=False
    )

    for doc in response['hits']['hits']:
        print(doc["fields"]["file"])
        print(doc["_score"])
        print(doc["fields"]["my_text"][0])
        print()