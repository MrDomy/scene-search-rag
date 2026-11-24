import numpy as np

def ranking(scores):
    return [int(i) for i in np.argsort(scores)[::-1]]

def best_result(scores, chunks, k=5):
    return [chunks[i] for i in ranking(scores)[:k]]


