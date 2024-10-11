import logging.config
import os
import yaml
from pathlib import Path

env = os.environ.get("APP_ENV")
if env == "local":
    from utils.constants import APP_ENV
    from app_config_loader import AppConfigLoader
else:
    from .utils.constants import APP_ENV
    from .app_config_loader import AppConfigLoader


def configure_logging():
    # read the logging.yaml file in the same directory as this file
    logging_config = os.path.join(Path(__file__).parent, 'logging.yaml')
    with open(logging_config, 'rt') as f:
        config = yaml.safe_load(f.read())

    # Configure the logging module with the config file
    logging.config.dictConfig(config)


def configure_application():
    env_val = os.environ.get(APP_ENV)

    file_name = 'application.yaml' if env_val == None else f'application-{env_val}.yaml'
    logging.info(f"loading {file_name}")
    application_file_path = os.path.join(Path(__file__).parent, file_name)
    config_loader = AppConfigLoader(application_file_path)
    config_loader.load_config()

    # For demonstration purposes, print the environment variables related to the app config
    for key in os.environ:
        if key.startswith('LLM'):
            print(f"{key}: {os.environ[key]}")