import faiss
import numpy as np
import os
import pickle

class FAISSVectorStore:
    def __init__(self, dim=384, index_file="faiss_index.index", meta_file="metadata.pkl"):
        self.dim = dim
        self.index_file = index_file
        self.meta_file = meta_file
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

        # Load if already exists
        if os.path.exists(index_file) and os.path.exists(meta_file):
            self.index = faiss.read_index(index_file)
            with open(meta_file, "rb") as f:
                self.metadata = pickle.load(f)

    def reset(self):
        # 🔄 Clear index and metadata
        self.index = faiss.IndexFlatL2(self.dim)
        self.metadata = []
        if os.path.exists(self.index_file):
            os.remove(self.index_file)
        if os.path.exists(self.meta_file):
            os.remove(self.meta_file)

    def add_texts(self, texts, embeddings):
        self.index.add(np.array(embeddings))
        self.metadata.extend(texts)

        # Save index and metadata
        faiss.write_index(self.index, self.index_file)
        with open(self.meta_file, "wb") as f:
            pickle.dump(self.metadata, f)

    def search(self, query_embedding, k=3):
        D, I = self.index.search(np.array([query_embedding]), k)
        return [self.metadata[i] for i in I[0] if i < len(self.metadata)]
