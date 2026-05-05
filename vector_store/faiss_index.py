import faiss
import numpy as np

class FAISSIndex:
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)

    def add_vectors(self, vectors):
        vectors = np.array(vectors).astype("float32")
        self.index.add(vectors)

    def search(self, query_vector, k=5):
        query_vector = np.array([query_vector]).astype("float32")
        distances, indices = self.index.search(query_vector, k)
        return indices[0]