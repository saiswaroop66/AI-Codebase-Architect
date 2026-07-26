from pathlib import Path

from reader.important_files import IMPORTANT_FILES


MAX_FILE_SIZE = 50_000  # 50 KB


def read_repository_files(repo_path: Path) -> dict:
    """
    Read the contents of important files in a repository.
    """

    repository_files = {}

    for file_path in repo_path.rglob("*"):

        if not file_path.is_file():
            continue

        if file_path.name not in IMPORTANT_FILES:
            continue

        try:

            if file_path.stat().st_size > MAX_FILE_SIZE:
                continue

            content = file_path.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            repository_files[str(file_path.relative_to(repo_path))] = content

        except Exception:
            continue

    return repository_files