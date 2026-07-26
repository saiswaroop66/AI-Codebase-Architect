from pathlib import Path

from scanner.ignore import IGNORE_FOLDERS, IGNORE_FILES
from scanner.language_detector import detect_language


def scan_repository(repo_path: Path) -> dict:
    """
    Scan a repository and collect basic information.
    """

    total_files = 0
    total_folders = 0
    total_size = 0

    languages = {}

    files = []

    for item in repo_path.rglob("*"):

        if item.is_dir():

            if item.name in IGNORE_FOLDERS:
                continue

            total_folders += 1

        elif item.is_file():

            if item.name in IGNORE_FILES:
                continue

            total_files += 1

            file_size = item.stat().st_size
            total_size += file_size

            language = detect_language(item)

            languages[language] = languages.get(language, 0) + 1

            files.append(
                {
                    "name": item.name,
                    "path": str(item.relative_to(repo_path)),
                    "language": language,
                    "size": file_size,
                }
            )

    return {
        "total_files": total_files,
        "total_folders": total_folders,
        "total_size": total_size,
        "languages": languages,
        "files": files,
    }