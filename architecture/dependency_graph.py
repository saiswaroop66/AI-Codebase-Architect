from pathlib import Path
import ast


class DependencyGraph:

    def __init__(self):
        self.graph = {}

    def build(self, repo_path: Path):
        """
        Build dependency graph for all Python files.
        """

        self.graph = {}

        python_files = list(repo_path.rglob("*.py"))

        for file in python_files:

            relative_path = file.relative_to(repo_path)

            try:

                source = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                tree = ast.parse(source)

            except Exception:

                continue

            imports = []

            for node in ast.walk(tree):

                if isinstance(node, ast.Import):

                    for alias in node.names:

                        imports.append(alias.name)

                elif isinstance(node, ast.ImportFrom):

                    module = node.module if node.module else ""

                    imports.append(module)

            self.graph[str(relative_path)] = imports

        return self.graph