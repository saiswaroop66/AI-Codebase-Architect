from pathlib import Path

from ai.groq_client import GroqClient


class FileExplainer:

    def __init__(self):

        self.llm = GroqClient()

    def explain(self, file_path: Path):

        try:

            content = file_path.read_text(
                encoding="utf-8",
                errors="ignore"
            )

        except Exception:

            return "Unable to read file."

        prompt = f"""
You are an expert software engineer.

Explain this source file.

Include:

1. Purpose
2. Important functions/classes
3. Workflow
4. Suggestions

----------------------

{content}

----------------------
"""

        return self.llm.invoke(prompt)