import networkx as nx


class InferenceEngine:

    SENSITIVITY_ORDER = {
        "public": 1,
        "internal": 2,
        "confidential": 3,
        "restricted": 4,
        # Legacy aliases kept for backwards compat
        "low": 1,
        "medium": 2,
        "high": 3,
        "critical": 4,
    }

    @classmethod
    def escalate_sensitivity(
        cls,
        graph: nx.DiGraph,
        detected_entities: list
    ):

        results = {}

        for entity in detected_entities:

            if entity not in graph.nodes:
                continue

            node_data = graph.nodes[entity]
            base_sensitivity = node_data.get("sensitivity", "public")
            final_sensitivity = base_sensitivity

            connected_nodes = list(graph.successors(entity))

            # FIX: collect full reasoning per edge before any variable is overwritten
            reasoning = []

            for connected in connected_nodes:

                edge_data = graph.get_edge_data(entity, connected)

                if edge_data["weight"] >= 0.8:

                    connected_sensitivity = graph.nodes[connected].get("sensitivity", "public")

                    if (
                        cls.SENSITIVITY_ORDER.get(connected_sensitivity, 0)
                        > cls.SENSITIVITY_ORDER.get(final_sensitivity, 0)
                    ):
                        final_sensitivity = connected_sensitivity

                reasoning.append({
                    "connected_entity": connected,
                    "relationship": edge_data["relationship"],
                    "weight": edge_data["weight"],
                    "triggered_escalation": edge_data["weight"] >= 0.8,
                })

            results[entity] = {
                "base_sensitivity": base_sensitivity,
                "final_sensitivity": final_sensitivity,
                "connected_entities": connected_nodes,
                "reasoning": reasoning,
            }

        return results
