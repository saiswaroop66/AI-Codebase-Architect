from pathlib import Path

from reader.file_reader import read_repository_files

from ai.groq_client import GroqClient

from review.prompts import CODE_REVIEW_PROMPT


class RepositoryReviewer:

    def __init__(self):

        self.llm = GroqClient()

    def review(self, repo_path: Path):

        files = read_repository_files(repo_path)

        repository = ""

        for file, content in files.items():

            repository += f"\n\nFILE: {file}\n"

            repository += content

        prompt = CODE_REVIEW_PROMPT.format(
            repository=repository
        )

        return self.llm.invoke(prompt)