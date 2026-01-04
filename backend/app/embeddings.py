 # backend/app/embeddings.py
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.preprocessing import normalize

MODEL_NAME = "all-MiniLM-L6-v2"  # CPU-friendly and small

class Embedder:
    def __init__(self, model_name=MODEL_NAME):
        self.model = SentenceTransformer(model_name)
    def embed_text(self, texts):
        # texts: list[str] or str
        if isinstance(texts, str):
            texts = [texts]
        emb = self.model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
        # L2-normalize for cosine sim via dot product
        emb = normalize(emb)
        return emb

