from pathlib import Path
import yaml


class RegistryLoader:

    @staticmethod
    def load_registry_files(registry_path: str):

        registry_data = []

        registry_dir = Path(registry_path)

        yaml_files = list(registry_dir.rglob("*.yaml")) + list(registry_dir.rglob("*.yml"))

        for yaml_file in sorted(set(yaml_files)):

            with open(yaml_file, "r", encoding="utf-8") as file:

                parsed = yaml.safe_load(file)

                if parsed and "nodes" in parsed:
                    registry_data.append(parsed)

        return registry_data
