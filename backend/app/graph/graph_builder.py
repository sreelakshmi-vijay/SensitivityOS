import yaml
import networkx as nx

from app.graph.models import SensitivityGraph


class GraphBuilder:

    @staticmethod
    def load_graph(path: str) -> nx.DiGraph:

        with open(path, "r") as file:
            data = yaml.safe_load(file)

        parsed_graph = SensitivityGraph(**data)

        graph = nx.DiGraph()

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