import math
from pathlib import Path

vector1 = [1, 2, 3]
vector2 = [4, 5, 6]

def cosine_similarity(a, b):
    result_dot_product = math.sumprod(a,b)

    length_a = math.hypot(*a)
    length_b = math.hypot(*b)
    if length_a == 0 or length_b == 0:
        return 0.0
    similarity = result_dot_product / (length_a * length_b)
    return similarity


def load_runbooks():
    doc_path = Path('docs')
    result = []
    for files in doc_path.rglob("*.md"):
        text = files.read_text(encoding="utf-8")
        result.append({"path" : str(files), "content" : text})
    return result

