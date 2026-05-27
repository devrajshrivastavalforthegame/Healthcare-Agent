import chromadb
import requests

client = chromadb.PersistentClient(path="./database")

collection = client.get_or_create_collection("healthcare")

with open("data/healthcare.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

for i, line in enumerate(lines):

    response = requests.post(
        OLLAMA_URL = "https://your-ngrok-url.ngrok-free.app",
        url=f"{OLLAMA_URL}/api/generate",
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