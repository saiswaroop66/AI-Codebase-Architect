from pathlib import Path

from reader.file_reader import read_repository_files
from ai.groq_client import GroqClient
from refactor.prompts import REFACTOR_PROMPT


class RefactoringAdvisor:

    def __init__(self):
        self.llm = GroqClient()

    def analyze(self, repo_path: Path):

        files = read_repository_files(repo_path)

        repository = ""

        for filename, content in files.items():

            repository += f"\n\nFILE: {filename}\n"

            repository += content

        prompt = REFACTOR_PROMPT.format(
            repository=repository
        )

        return self.llm.invoke(prompt)