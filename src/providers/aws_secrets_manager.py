"""
Mock module
"""

import boto3
import botocore

def create_secret(secret_name):
    """
    Mock Function
    """
    return f"{secret_name} secret created"

def update_secret(secret_name):
    """
    Mock Function
    """
    return f"{secret_name} secret updated"

def check_secret(client: boto3.client, secret_name: str):
    """
    Checks to see if the last updated time on a secret is older than 60 seconds
    """
    outcome = ""
    try:
        response = client.describe_secret(SecretId=secret_name)
        return response['LastChangedDate']
    except botocore.exceptions.ClientError as error :
        outcome = f"Error: {error}"

    return outcome


def create_client():
    """
    Mock Function
    """
    return "Client created"
