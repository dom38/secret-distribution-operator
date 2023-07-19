"""
Provides a global config object
"""

import yaml


class ConfigLoader:
    """
    A singleton class to load config from a file on startup.
    """
    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def load_config(cls):
        """
        Loads config from a file or memory.
        """
        if cls._config is None:
            with open('config/config.yaml', 'r', encoding="utf-8") as file:
                cls._config = yaml.safe_load(file)
        return dict(cls._config)
