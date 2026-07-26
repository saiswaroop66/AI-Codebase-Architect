from sentence_transformers import SentenceTransformer


class RepositoryRetriever:
    """
    Retrieves the most relevant code chunks from the vector store.
    """

    def __init__(self, vector_store):

        self.vector_store = vector_store

        self.embedding_model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    def retrieve(self, question: str, top_k: int = 5):
        """
        Retrieve the top matching chunks for a user question.
        """

        query_embedding = self.embedding_model.encode(
            question,
            convert_to_numpy=True
        )

        results = self.vector_store.search(
            query_embedding,
            top_k
        )

        return results