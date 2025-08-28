import os, json, faiss
from sentence_transformers import SentenceTransformer
def main():
    os.makedirs("data/index", exist_ok=True)
    emb = SentenceTransformer("BAAI/bge-small-en-v1.5")
    texts = ["Seed document for bootstrapping."]
    meta = {"0": {"source": "seed", "text": texts[0]}}
    vecs = emb.encode(texts, normalize_embeddings=True)
    index = faiss.IndexFlatIP(vecs.shape[1]); index.add(vecs)
    faiss.write_index(index, "data/index/faiss.index")
    with open("data/index/meta.json","w") as f: json.dump(meta,f)
    print("Index built.")
if __name__ == "__main__": main()
