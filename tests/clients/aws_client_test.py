"""
test src/clients/aws_client.py
"""

import unittest
from unittest.mock import MagicMock, patch
from src.clients.aws_client import ExternalServiceClient

class ExternalServiceClientTestCase(unittest.TestCase):
    """
    Class to contain test cases
    """

    def test_create_client_ssm_enabled(self):
        """
        Function to test SSM client creation
        """
        config = {
            "external_services": {
                "aws_parameter_store": {
                    "enabled": True
                }
            }
        }
        client_type = "ssm"

        with patch("src.clients.aws_client.ConfigLoader") as mock_config_loader, \
             patch("src.clients.aws_client.boto3.client") as mock_boto3_client:

            mock_config_loader.return_value.load_config.return_value = config
            mock_boto3_client.return_value = MagicMock()

            client = ExternalServiceClient.create_client(client_type)

            self.assertIsNotNone(client.client)
            mock_boto3_client.assert_called_once_with('ssm')

    def test_create_client_ssm_disabled(self):
        """
        Function to test SSM client not created
        """
        config = {
            "external_services": {
                "aws_parameter_store": {
                    "enabled": False
                }
            }
        }
        client_type = "ssm"

        with patch("src.clients.aws_client.ConfigLoader") as mock_config_loader, \
             patch("src.clients.aws_client.boto3.client") as mock_boto3_client:

            mock_config_loader.return_value.load_config.return_value = config
            mock_boto3_client.return_value = MagicMock()

            client = ExternalServiceClient.create_client(client_type)

            self.assertIsNone(client)
            mock_boto3_client.assert_not_called()

    def test_create_client_secretsmanager_enabled(self):
        """
        Function to test Secrets Manager client creation
        """
        config = {
            "external_services": {
                "aws_secrets_manager": {
                    "enabled": True
                }
            }
        }
        client_type = "secretsmanager"

        with patch("src.clients.aws_client.ConfigLoader.load_config") as mock_load_config, \
             patch("src.clients.aws_client.boto3.client") as mock_boto3_client:

            mock_load_config.return_value = config
            mock_boto3_client.return_value = MagicMock()

            client = ExternalServiceClient.create_client(client_type)

            self.assertIsNotNone(client.client)
            mock_boto3_client.assert_called_once_with('secretsmanager')

    def test_create_client_secretsmanager_disabled(self):
        """
        Function to test Secrets Manager client not created
        """
        config = {
            "external_services": {
                "aws_secrets_manager": {
                    "enabled": False
                }
            }
        }
        client_type = "secretsmanager"

        with patch("src.clients.aws_client.ConfigLoader.load_config") as mock_load_config, \
             patch("src.clients.aws_client.boto3.client") as mock_boto3_client:

            mock_load_config.return_value = config
            mock_boto3_client.return_value = MagicMock()

            client = ExternalServiceClient.create_client(client_type)

            self.assertIsNone(client)
            mock_boto3_client.assert_not_called()

    def test_create_client_first_instance(self):
        """
        Test client is created when no client exists
        """
        config = {
            "external_services": {
                "aws_parameter_store": {
                    "enabled": True
                }
            }
        }
        client_type = "ssm"

        with patch("src.clients.aws_client.ConfigLoader") as mock_config_loader, \
             patch("src.clients.aws_client.boto3.client") as mock_boto3_client:

            mock_config_loader.return_value.load_config.return_value = config
            mock_boto3_client.return_value = MagicMock()
            ExternalServiceClient._instance = None
            client = ExternalServiceClient(client_type)

            self.assertIsNotNone(client)
            self.assertIsNotNone(ExternalServiceClient._instance)
            self.assertIsInstance(client, ExternalServiceClient)
            self.assertEqual(client, ExternalServiceClient._instance)

            mock_boto3_client.assert_called_once_with('ssm')
