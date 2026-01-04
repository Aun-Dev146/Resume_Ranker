# backend/tests/test_embeddings.py
"""Test suite for embeddings module"""

import sys
import os
import numpy as np

# Add backend/app to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from embeddings import Embedder


def test_embedder_initialization():
    """Test that Embedder initializes correctly"""
    embedder = Embedder()
    assert embedder is not None
    assert embedder.model is not None
    print("✓ Embedder initialization test passed")


def test_single_text_embedding():
    """Test embedding a single text"""
    embedder = Embedder()
    text = "Python developer with machine learning experience"
    
    embedding = embedder.embed_text(text)
    
    assert embedding is not None
    assert len(embedding) == 1
    assert embedding[0].shape == (384,)  # all-MiniLM-L6-v2 uses 384 dimensions
    assert np.isclose(np.linalg.norm(embedding[0]), 1.0)  # Check L2 normalization
    print("✓ Single text embedding test passed")


def test_multiple_texts_embedding():
    """Test embedding multiple texts"""
    embedder = Embedder()
    texts = [
        "Senior Python developer",
        "Java backend engineer",
        "Frontend web developer"
    ]
    
    embeddings = embedder.embed_text(texts)
    
    assert len(embeddings) == 3
    for emb in embeddings:
        assert emb.shape == (384,)
        assert np.isclose(np.linalg.norm(emb), 1.0)
    print("✓ Multiple texts embedding test passed")


def test_cosine_similarity():
    """Test cosine similarity calculation"""
    embedder = Embedder()
    
    # Similar texts should have high similarity
    text1 = "Python developer"
    text2 = "Python programmer"
    
    emb1 = embedder.embed_text(text1)[0]
    emb2 = embedder.embed_text(text2)[0]
    
    similarity = np.dot(emb1, emb2)
    assert 0.5 < similarity < 1.0
    print(f"✓ Cosine similarity test passed (similarity: {similarity:.4f})")


def test_dissimilar_texts():
    """Test that very different texts have low similarity"""
    embedder = Embedder()
    
    text1 = "Python developer"
    text2 = "Cooking recipe for pasta"
    
    emb1 = embedder.embed_text(text1)[0]
    emb2 = embedder.embed_text(text2)[0]
    
    similarity = np.dot(emb1, emb2)
    assert 0 < similarity < 0.3  # Should be quite different
    print(f"✓ Dissimilar texts test passed (similarity: {similarity:.4f})")


def run_all_tests():
    """Run all embedding tests"""
    print("\n" + "="*50)
    print("Running Embedding Tests")
    print("="*50 + "\n")
    
    try:
        test_embedder_initialization()
        test_single_text_embedding()
        test_multiple_texts_embedding()
        test_cosine_similarity()
        test_dissimilar_texts()
        
        print("\n" + "="*50)
        print("✓ All tests passed!")
        print("="*50 + "\n")
        return True
    
    except Exception as e:
        print(f"\n✗ Test failed: {str(e)}")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
