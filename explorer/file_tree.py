from pathlib import Path

IGNORE_FOLDERS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    ".idea",
    ".vscode",
    "dist",
    "build"
}


def get_repository_tree(repo_path: Path):
    """
    Return all repository files in a tree structure.
    """

    tree = []

    for path in sorted(repo_path.rglob("*")):

        relative_path = path.relative_to(repo_path)

        # Skip ignored folders
        if any(part in IGNORE_FOLDERS for part in relative_path.parts):
            continue

        tree.append({
            "name": path.name,
            "path": str(relative_path),
            "is_file": path.is_file()
        })

    return tree