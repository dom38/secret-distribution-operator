"""
Module to create secrets manager client
"""

import boto3
from config import ConfigLoader

class ExternalServiceClient:
    """
    Creates a singleton external service client based on the client type
    """

    _instance = None

    def __new__(cls, client_type):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = cls.create_client(client_type)
        return cls._instance

    @staticmethod
    def create_client(client_type):
        """
        Conditionally creates the client based on the client type and config
        """
        config_loader = ConfigLoader()
        config = config_loader.load_config()
        client = None

        if client_type == "ssm" and config["external_services"]["aws_parameter_store"]["enabled"]:
            client = boto3.client('ssm')
        elif client_type == "secretsmanager" and config["external_services"]["aws_secrets_manager"]["enabled"]:
            client = boto3.client('secretsmanager')

        return client
