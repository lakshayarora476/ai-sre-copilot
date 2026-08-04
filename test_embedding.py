from app.embedding_client import get_embedding

embedding = get_embedding("my app is running out of RAM")

print("Embedding length:", len(embedding))
print("First 5 values:", embedding[:5])
