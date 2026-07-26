from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter


class RepositoryChunker:
    """
    Splits repository files into smaller chunks for embeddings.
    """

    def __init__(self):

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    def chunk_repository(self, repository_files: dict):
        """
        Convert repository files into chunks.
        """

        chunks = []

        for filename, content in repository_files.items():

            split_text = self.text_splitter.split_text(content)

            for i, chunk in enumerate(split_text):

                chunks.append({
                    "file": filename,
                    "chunk_id": i,
                    "content": chunk
                })

        return chunks