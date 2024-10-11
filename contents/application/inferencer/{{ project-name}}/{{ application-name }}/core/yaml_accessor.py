import os

import yaml


class YamlAccessor:
    def __init__(self, filepath):
        """
        Initializes the YamlAccessor with the path to the YAML file.

        :param filepath: Path to the YAML file.
        """
        self.filepath = filepath

    def read(self):
        """
        Reads the YAML file and returns the data as a Python dictionary.

        :return: A dictionary containing the YAML content.
        """
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"YAML file not found: {self.filepath}")

        with open(self.filepath, 'r') as file:
            data = yaml.safe_load(file)
        return data

    def write(self, data):
        """
        Writes a Python dictionary to the YAML file.

        :param data: The Python dictionary to serialize to YAML.
        """
        with open(self.filepath, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)
