import networkx as nx

from app.graph.models import SensitivityGraph
from app.graph.registry_loader import RegistryLoader


class GraphBuilder:

    @staticmethod
    def load_graph(registry_path: str) -> nx.DiGraph:

        graph = nx.DiGraph()

        registry_files = RegistryLoader.load_registry_files(
            registry_path
        )

        for registry in registry_files:

            parsed_graph = SensitivityGraph(**registry)

            for node in parsed_graph.nodes:

                graph.add_node(
                    node.id,
                    category=node.category,
                    sensitivity=node.sensitivity
                )

            for edge in parsed_graph.edges:

                graph.add_edge(
                    edge.source,
                    edge.target,
                    relationship=edge.relationship,
                    weight=edge.weight
                )

        return graph