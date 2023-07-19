from contextlib import contextmanager
import unittest
from unittest.mock import patch
import pytest
from src.config import ConfigLoader

@contextmanager
def mock_open(config_content):
    try:
        yield config_content
    finally:
        pass

@pytest.fixture
def mock_open_config(monkeypatch):
    config_content = """
    key1: value1
    key2: value2
    """

    monkeypatch.setattr('builtins.open', lambda *args, **kwargs: mock_open(config_content))

@pytest.fixture
def config_loader(mock_open_config):
    return ConfigLoader()

def test_load_config(config_loader):
    # Load the config
    config = config_loader.load_config()

    # Assert that the config is loaded and of the expected type
    assert isinstance(config, dict)
    # Add additional assertions based on your config structure and content
    assert "key1" in config
    assert config["key1"] == "value1"


# class ConfigLoaderTestCase(unittest.TestCase):

#     def test_load_config(self):
#         # Create an instance of ConfigLoader
#         config_loader = ConfigLoader()

#         # Load the config
#         config = config_loader.load_config()

#         # Assert that the config is loaded and of the expected type
#         self.assertIsInstance(config, dict)
        