from embanding import query_vec, chunk_vecs
from chunker import get_chunks

from multiplication import get_score
from filter import ranking
import eval_queries

def normalize(text: str) -> str:
    return ' '.join(text.lower().replace('ё', 'е').split())

def relevant_ids(chunks: list[str], spans: list[str]) -> set[int]:
    '''принимает чанки и верные фрагменты чанков. Возвращает номера чанков, в которых нашлись верные фрагменты'''
    result = set()
    for i, chunk in enumerate(chunks):
        chunk = normalize(chunk)
        if any(normalize(span) in chunk for span in spans):
            result.add(i)
    return result

def hit_at_k(ranked: list[int], relevant: set[int], k: int) -> float:
    for chunk_num in ranked[:k]:
        if chunk_num in relevant: return 1.0
    return 0.0

def reciprocal_rank(ranked: list[int], relevant: set[int]) -> float:
    for place, chunk_num in enumerate(ranked, start=1):
        if chunk_num in relevant:
            return 1/place
    return 0.0

def evaluate(chunks, vecs, queries):
    h1, h3, h5, rr = [], [], [], []
    for query in queries:
        correct_chunks = relevant_ids(chunks, query['spans'])
        if not correct_chunks:
            print('Пропуск (цитата не найдена):', query['query'])
            continue

        current_query_vec = query_vec(query['query'])
        found_chunks = ranking(get_score(current_query_vec, vecs))

        rr_score = reciprocal_rank(found_chunks, correct_chunks)
        place = round(1 / rr_score) if rr_score > 0 else None
        print(f'Место {place}: {query["query"]}')

        h1.append(hit_at_k(found_chunks, correct_chunks, 1))
        h3.append(hit_at_k(found_chunks, correct_chunks, 3))
        h5.append(hit_at_k(found_chunks, correct_chunks, 5))
        rr.append(rr_score)

    n = len(rr)
    if n == 0:
        print('Ни один запрос не попал в оценку.')
        return

    print(f'\nЗапросов в оценке: {n}')
    print(f'Hit@1: {sum(h1) / n:.3f}')
    print(f'Hit@3: {sum(h3) / n:.3f}')
    print(f'Hit@5: {sum(h5) / n:.3f}')
    print(f'MRR:   {sum(rr) / n:.3f}')

    print(f'h1 - {h1}\nh3 - {h3}\nh5 - {h5}\nrr - {rr}\n')

if __name__ == "__main__":
    chunks = get_chunks("fics/all_sheckley_stories.txt")
    vecs = chunk_vecs(chunks)
    evaluate(chunks, vecs, eval_queries.QUERIES)
