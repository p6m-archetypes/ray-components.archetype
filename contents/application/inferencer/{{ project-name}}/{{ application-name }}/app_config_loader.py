import os
env = os.environ.get("APP_ENV")
if env == "local":
    from core.yaml_accessor import YamlAccessor
else:
    from .core.yaml_accessor import YamlAccessor


class AppConfigLoader:
    def __init__(self, config_path):
        self.config_path = config_path

    def load_config(self):
        """
        Loads the configuration from a YAML file and sets environment variables accordingly.
        """
        accessor = YamlAccessor(self.config_path)
        config = accessor.read()

        # Assuming the configuration has a specific top-level key for environment variables, e.g., 'env'
        if 'env' in config:
            self._set_env_vars(config['env'])

    def _set_env_vars(self, config, prefix=''):
        """
        Recursively sets environment variables based on the nested dictionary structure.

        :param config: The nested dictionary portion of the configuration.
        :param prefix: The accumulated prefix for the environment variable names.
        """
        if isinstance(config, dict):
            for key, value in config.items():
                new_prefix = f"{prefix}{key}."
                self._set_env_vars(value, new_prefix)
        else:
            # Trim the last underscore and set the environment variable
            env_var_name = prefix[:-1]  # Remove the trailing underscore
            os.environ[env_var_name] = str(config)
