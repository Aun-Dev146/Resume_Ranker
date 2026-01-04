import sys
import os
import numpy as np

try:
    print("Python version:", sys.version)
    print("Current working directory:", os.getcwd())
    print("Python path:", sys.path)

    # --- Ensure backend/app is importable ---
    backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend/app'))
    print("Adding to path:", backend_path)
    sys.path.append(backend_path)
    
    print("Attempting to import sentence_transformers...")
    import sentence_transformers
    print("sentence_transformers imported successfully")

except Exception as e:
    print("Error occurred:", str(e))
    sys.exit(1)

# --- Import Embedder class ---
from embeddings import Embedder

# --- Create instance of Embedder ---
print("Loading the embedding model...")
embedder = Embedder()
print("Model loaded successfully!")

# --- Sample texts for testing ---
text1 = "Experienced Python developer skilled in FastAPI and machine learning."
text2 = "AI engineer proficient in Python, backend development, and data processing."

# --- Get embeddings ---
vecs = embedder.embed_text([text1, text2])
vec1, vec2 = vecs[0], vecs[1]

# --- Print shapes ---
print("Embedding 1 shape:", vec1.shape)
print("Embedding 2 shape:", vec2.shape)

# --- Compute cosine similarity manually ---
cos_sim = np.dot(vec1, vec2)

print("\nCosine Similarity:", round(float(cos_sim), 4))
 
