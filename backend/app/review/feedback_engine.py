from pathlib import Path
import yaml


class FeedbackEngine:

    @staticmethod
    def update_graph_weights(
        registry_path: str,
        decision
    ):

        registry_file = Path(registry_path)

        with open(registry_file, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        updated = False

        for edge in data.get("edges", []):

            # FIX: match on source + target, not just relationship string
            # This prevents spurious updates when multiple edges share a relationship type
            if (
                edge.get("source") == decision.entity
                and edge.get("target") == decision.corrected_sensitivity
            ) or (
                edge.get("relationship") == decision.relationship
                and edge.get("source") == decision.entity
            ):
                edge["weight"] = round(
                    min(edge["weight"] + decision.confidence_adjustment, 1.0), 4
                )
                updated = True

        if updated:

            with open(registry_file, "w", encoding="utf-8") as file:
                yaml.dump(data, file, sort_keys=False, allow_unicode=True)

        return {"updated": updated}
