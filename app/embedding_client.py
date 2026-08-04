import requests

EMBEDDING_URL = "http://127.0.0.1:8080/v1/embeddings"

def get_embedding(text):
    payload = {
        "input": text,
        "model": "qwen",
    }

    response = requests.post(
        EMBEDDING_URL,
        json=payload,
        timeout=60,
    )

    if response.status_code != 200:
        raise RuntimeError(f"Embedding API failed: {response.text}")

    data = response.json()
    return data["data"][0]["embedding"]