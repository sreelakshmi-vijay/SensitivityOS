import yaml


class FeedbackEngine:

    @staticmethod
    def update_graph_weights(
        registry_path: str,
        decision
    ):

        with open(registry_path, "r") as file:

            data = yaml.safe_load(file)

        updated = False

        for edge in data.get("edges", []):

            if edge["relationship"] == decision.relationship:

                edge["weight"] += decision.confidence_adjustment

                edge["weight"] = min(edge["weight"], 1.0)

                updated = True

        if updated:

            with open(registry_path, "w") as file:

                yaml.dump(data, file, sort_keys=False)

        return {
            "updated": updated
        }