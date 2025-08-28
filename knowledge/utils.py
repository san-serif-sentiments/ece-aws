import faiss, os, json
import numpy as np
from sentence_transformers import SentenceTransformer
_EMB=_INDEX=_META=None
def _load(persist="data/index"):
    global _EMB,_INDEX,_META
    if _EMB is None: _EMB=SentenceTransformer("BAAI/bge-small-en-v1.5")
    if _INDEX is None: _INDEX=faiss.read_index(os.path.join(persist,"faiss.index"))
    if _META is None:
        with open(os.path.join(persist,"meta.json"),"r",encoding="utf-8") as f:
            _META=json.load(f)
def embed(texts):
    global _EMB
    if _EMB is None: _EMB=SentenceTransformer("BAAI/bge-small-en-v1.5")
    return _EMB.encode(texts, normalize_embeddings=True)
def retrieve_chunks(query,k=10,persist="data/index"):
    _load(persist); qv=embed([query]).astype("float32")
    scores,idxs=_INDEX.search(np.array(qv),k)
    return [{"text":_META[str(i)]["text"],"source":_META[str(i)]["source"]} for i in idxs[0]]
