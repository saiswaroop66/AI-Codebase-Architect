from pathlib import Path
import ast


class CallGraph:

    def __init__(self):
        self.graph = {}

    def build(self, repo_path: Path):
        """
        Build function call graph for all Python files.
        """

        self.graph = {}

        python_files = list(repo_path.rglob("*.py"))

        for file in python_files:

            try:

                source = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                tree = ast.parse(source)

            except Exception:
                continue

            file_calls = {}

            for node in ast.walk(tree):

                if isinstance(node, ast.FunctionDef):

                    function_name = node.name

                    calls = []

                    for child in ast.walk(node):

                        if isinstance(child, ast.Call):

                            if isinstance(child.func, ast.Name):

                                calls.append(child.func.id)

                            elif isinstance(child.func, ast.Attribute):

                                calls.append(child.func.attr)

                    file_calls[function_name] = calls

            self.graph[str(file.relative_to(repo_path))] = file_calls

        return self.graph