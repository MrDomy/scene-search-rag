from chunker import get_chunks
from embanding import chunk_vecs, query_vec
from multiplication import get_score
from filter import best_result
from llm_processing import get_responce

# что если сам запрос больше 190 символов?

chunks = get_chunks("fics/all_sheckley_stories.txt")
#print(chunks[:10])
vecs = chunk_vecs(chunks)
print("Ну хз, попробуй что-нибудь ввести")
query = input()
qvec = query_vec(query)
score = get_score(qvec, vecs)
responce = get_responce(best_result(score, chunks), query)
print(responce)



