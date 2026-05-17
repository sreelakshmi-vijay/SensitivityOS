import networkx as nx


class InferenceEngine:

    SENSITIVITY_ORDER = {
        "low": 1,
        "medium": 2,
        "high": 3,
        "critical": 4
    }

    @classmethod
    def escalate_sensitivity(
        cls,
        graph: nx.DiGraph,
        detected_entities: list[str]
    ):

        results = {}

        for entity in detected_entities:

            if entity not in graph.nodes:
                continue

            base_sensitivity = graph.nodes[entity]["sensitivity"]
            final_sensitivity = base_sensitivity

            connected_nodes = list(graph.successors(entity))

            for connected in connected_nodes:

                edge_data = graph.get_edge_data(entity, connected)

                if edge_data["weight"] >= 0.8:

                    connected_sensitivity = graph.nodes[connected]["sensitivity"]

                    if (
                        cls.SENSITIVITY_ORDER[connected_sensitivity]
                        >
                        cls.SENSITIVITY_ORDER[final_sensitivity]
                    ):
                        final_sensitivity = connected_sensitivity

            results[entity] = {
                "base_sensitivity": base_sensitivity,
                "final_sensitivity": final_sensitivity,
                "connected_entities": connected_nodes
            }

        return results