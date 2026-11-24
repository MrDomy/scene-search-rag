from sentence_transformers import SentenceTransformer
import numpy as np
from pathlib import Path

model = SentenceTransformer('intfloat/multilingual-e5-small')   # один раз при импорте


def chunk_vecs(chunks, mode = ''):
    if Path("vecs.npy").exists() and mode != "encode":
        return np.load("vecs.npy")
    else:
        texts = ["passage: " + c for c in chunks]
        res = model.encode(texts, normalize_embeddings=True, show_progress_bar=True)
        np.save("vecs.npy", res)
        return res
    
def query_vec(query: str):
    model = SentenceTransformer('intfloat/multilingual-e5-small')
    return model.encode("query: " + query, normalize_embeddings=True, show_progress_bar=True)