import json, faiss, numpy as np
from sentence_transformers import SentenceTransformer
def research(query, k=6):
    emb = SentenceTransformer("BAAI/bge-small-en-v1.5")
    index = faiss.read_index("data/index/faiss.index")
    meta = json.load(open("data/index/meta.json"))
    q = emb.encode([query], normalize_embeddings=True).astype("float32")
    scores, idxs = index.search(np.array(q), k)
    return [{"text": meta[str(i)]["text"], "source": meta[str(i)]["source"]} for i in idxs[0]]
