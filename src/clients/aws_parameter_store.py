import boto3
from config import load_config

class ParameterStoreClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = cls.create_client()
        return cls._instance

    @staticmethod
    def create_client():
        config = load_config()
        if config["external_services"]["aws_parameter_store"]["enabled"]:
            return boto3.client('ssm')
        else:
            return None
