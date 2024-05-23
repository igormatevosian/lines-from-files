import yaml
from yaml.loader import SafeLoader


class ConfigLoader:
    def __init__(self, config_file: str, config_id: int) -> None:
        self.config_file = config_file
        self.config_id = config_id

        try:
            with open(config_file, 'r') as file:
                configurations = yaml.load(
                    file, Loader=SafeLoader).get('configurations', {})
                if config_id not in configurations:
                    raise ValueError(
                        f"Configuration ID {config_id} not found in the configuration file.")
                data = configurations[config_id]
                self.mode: str = data['mode']
                self.path: list[str] = data['path']
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Configuration file {config_file} not found.")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file: {e}")

    def __str__(self) -> str:
        return f"ConfigLoader(config_file='{self.config_file}', config_id={self.config_id}, mode='{self.mode}', path='{self.path}')"

    def __repr__(self) -> str:
        return self.__str__()
