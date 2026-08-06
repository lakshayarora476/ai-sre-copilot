from app.embedding_client import get_embedding
from app.semantic_retrieval import cosine_similarity


text_1 = "my app is running out of RAM"
text_2 = "container uses too much memory"

embedding_1 = get_embedding(text_1)
embedding_2 = get_embedding(text_2)

score = cosine_similarity(embedding_1, embedding_2)

print("Similarity score:", score)