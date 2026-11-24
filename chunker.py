from pathlib import Path
CHUNK = 150
STEP = 120


def get_chunks(link: str, chunk_size: int = CHUNK, step: int = STEP):
    text = Path(link).read_text(encoding="utf-8")
    words = text.split()
    chunks = []
    for i in range(0, len(words), step):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks
