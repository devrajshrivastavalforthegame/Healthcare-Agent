from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
import requests

# Load embeddings
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# Load FAISS database
db = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

# User Question
query = input("Ask your healthcare question: ")

# Similarity Search
results = db.similarity_search(query, k=2)

# Extract Context
context = "\n".join(
    [doc.page_content for doc in results]
)

print("\nRetrieved Context:\n")
print(context)

# Create Prompt
prompt = f"""
You are a healthcare navigation assistant.

Context:
{context}

Question:
{query}

Instructions:
- Give educational guidance only
- Do not provide exact diagnosis
- Recommend doctors if needed
- Mention emergency warning signs
"""

# Send to 
print("Sending request to llama3...")
response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }
)
print("Response received!")

answer = response.json()["response"]

print("\nAI Response:\n")
print(answer)