from pathlib import Path

from reader.file_reader import read_repository_files


def build_repository_context(repo_path: Path) -> str:
    """
    Build a clean repository context for the LLM.
    """

    files = read_repository_files(repo_path)

    context = []

    context.append("=" * 60)
    context.append(f"Repository: {repo_path.name}")
    context.append("=" * 60)

    for filename, content in files.items():

        context.append(f"\nFILE: {filename}")
        context.append("-" * 60)

        context.append(content)

        context.append("\n")

    return "\n".join(context)