class ArchitectureDiagram:
    """
    Generate Mermaid diagrams from dependency graphs.
    """

    def generate(self, dependency_graph):

        diagram = ["graph TD"]

        for file, dependencies in dependency_graph.items():

            source = self.clean_name(file)

            for dependency in dependencies:

                target = self.clean_name(dependency)

                diagram.append(f"{source} --> {target}")

        return "\n".join(diagram)

    def clean_name(self, name):

        return (
            name.replace("/", "_")
                .replace("\\", "_")
                .replace(".", "_")
                .replace("-", "_")
        )