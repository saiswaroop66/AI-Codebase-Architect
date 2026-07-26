from ai.groq_client import GroqClient
from ai.prompts import REPOSITORY_SUMMARY_PROMPT
from reader.context_builder import build_repository_context


class RepositoryAnalyzer:

    def __init__(self):
        self.client = GroqClient()

    def analyze(self, repo_path):

        context = build_repository_context(repo_path)

        prompt = REPOSITORY_SUMMARY_PROMPT.format(
            repository_info=context
        )

        return self.client.invoke(prompt)