import math

def cosine_similarity(vector_a, vector_b):
    dot_product = 0
    norm_a = 0
    norm_b = 0

    for a, b in zip(vector_a, vector_b):
        dot_product += a * b
        norm_a += a * a
        norm_b += b * b

    if norm_a == 0 or norm_b == 0:
        return 0

    return dot_product / (math.sqrt(norm_a) * math.sqrt(norm_b))