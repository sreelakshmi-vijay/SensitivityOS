from pathlib import Path
import yaml


class RegistryLoader:

    @staticmethod
    def load_registry_files(registry_path: str):

        registry_data = []

        yaml_files = Path(registry_path).rglob("*.yaml")

        for yaml_file in yaml_files:

            with open(yaml_file, "r") as file:

                parsed = yaml.safe_load(file)

                registry_data.append(parsed)

        return registry_data