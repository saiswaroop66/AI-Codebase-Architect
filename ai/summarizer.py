from ai.groq_client import GroqClient
from ai.prompts import DOCUMENTATION_PROMPT


class RepositorySummarizer:
    """
    Generate professional documentation and summaries
    for a repository.
    """

    def __init__(self):
        self.client = GroqClient()

    def generate_summary(self, repository_data: dict) -> str:
        """
        Generate repository documentation.
        """

        prompt = DOCUMENTATION_PROMPT.format(
            repository_info=repository_data
        )

        response = self.client.invoke(prompt)

        return response