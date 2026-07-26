from pathlib import Path
from git import Repo, GitCommandError

from config.settings import REPOSITORY_DIR


def clone_repository(repo_url: str) -> Path:
    """
    Clone a GitHub repository if it doesn't already exist.
    If it already exists, reuse the local copy.
    """

    repo_url = repo_url.splitlines()[0].strip()

    repo_name = repo_url.rstrip("/").split("/")[-1]

    clone_path = REPOSITORY_DIR / repo_name

    # Repository already exists
    if clone_path.exists():
        return clone_path

    try:
        Repo.clone_from(
            repo_url,
            clone_path,
            depth=1      # Shallow clone (faster)
        )

    except GitCommandError as e:
        raise Exception(f"Failed to clone repository:\n{e}")

    return clone_path