import chromadb
import requests

client = chromadb.PersistentClient(path="./database")

collection = client.get_or_create_collection("healthcare")

with open("data/healthcare.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

for i, line in enumerate(lines):

    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": line
        }
    )

    embedding = response.json()["embedding"]

    collection.add(
        ids=[str(i)],
        embeddings=[embedding],
        documents=[line]
    )

print("Embeddings stored successfully!")