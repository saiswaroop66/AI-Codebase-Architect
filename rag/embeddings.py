from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:
    """
    Generates embeddings for repository chunks.
    """

    def __init__(self):
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    def create_embeddings(self, chunks):
        """
        Convert text chunks into vector embeddings.
        """

        texts = [chunk["content"] for chunk in chunks]

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True
        )

        return embeddings