import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


class GroqClient:
    """
    Handles communication with the Groq LLM.
    """

    def __init__(self):

        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model=os.getenv("GROQ_MODEL"),
            temperature=0
        )

    def invoke(self, prompt: str) -> str:
        """
        Send a prompt to the model and return the response.
        """

        response = self.llm.invoke(prompt)

        return response.content