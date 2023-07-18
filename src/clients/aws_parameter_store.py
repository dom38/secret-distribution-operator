"""
Module to create param store client
"""

import boto3
from config import load_config

class ParameterStoreClient:
    """
    Creates a singelton param store client 
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = cls.create_client()
        return cls._instance

    @staticmethod
    def create_client():
        """
        Conditionally creates client depending on config
        """
        config = load_config()
        client = ""
        if config["external_services"]["aws_parameter_store"]["enabled"]:
            client = boto3.client('ssm')
        else:
            client = None
        return client
