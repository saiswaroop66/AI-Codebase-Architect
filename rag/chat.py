from rag.retriever import RepositoryRetriever
from ai.groq_client import GroqClient


class RepositoryChat:

    def __init__(self, vector_store):

        self.retriever = RepositoryRetriever(vector_store)
        self.llm = GroqClient()

    def ask(self, question):

        retrieved_chunks = self.retriever.retrieve(question)

        context = ""

        for chunk in retrieved_chunks:

            context += (
                f"\n\nFILE: {chunk['file']}\n"
                f"{chunk['content']}"
            )

        prompt = f"""
You are an expert Software Architect.

Answer the user's question ONLY using the repository context below.

If the answer is not found, say:
"I couldn't find this information in the repository."

==============================
Repository Context
==============================

{context}

==============================
User Question
==============================

{question}

==============================
Answer
==============================
"""

        response = self.llm.invoke(prompt)

        return response