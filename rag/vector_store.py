import faiss
import numpy as np


class VectorStore:
    """
    Stores and searches repository embeddings using FAISS.
    """

    def __init__(self):

        self.index = None
        self.chunks = []

    def build_index(self, embeddings, chunks):
        """
        Build the FAISS index from embeddings.
        """

        embeddings = np.array(embeddings).astype("float32")

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)

        self.index.add(embeddings)

        self.chunks = chunks

    def search(self, query_embedding, top_k=5):
        """
        Search the most similar chunks.
        """

        query_embedding = np.array([query_embedding]).astype("float32")

        distances, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for idx in indices[0]:

            if idx < len(self.chunks):

                results.append(self.chunks[idx])

        return results