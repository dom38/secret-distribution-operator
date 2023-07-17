import kopf
from providers import aws_secrets_manager
import yaml
import json
import boto3

def namespace_inclusion(namespace, memo: kopf.Memo, **_): 

    if namespace in memo.global_config["kubernetes"]["excluded_namespaces"]:
        return False
    
    if len(memo.global_config["kubernetes"]["included_namespaces"]) == 0:
        return True
    
    if namespace in memo.global_config["kubernetes"]["included_namespaces"]:
        return True

def get_annotation(annotations, **_): return annotations.get('dom.dev/distribute') == 'true'

@kopf.on.startup()
def start_background_worker(memo: kopf.Memo, logger, **_):
    config = yaml.safe_load(open('config/config.yaml'))
    logger.info(f"config: {json.dumps(config)}")
    memo.global_config = config
    global secrets_manager_client 
    secrets_manager_client = boto3.client("secretsmanager")

@kopf.on.create('secret', 
                when=kopf.any_([
                    namespace_inclusion,
                    get_annotation,
                    ])
                )
def create_fn(memo: kopf.Memo, name, body, logger, **_):
    result = aws_secrets_manager.create_secret(name)
    logger.info(f"Config: {memo.global_config}")
    logger.info(f"Result: {result}")
    logger.info(f"Secret: {body}")

@kopf.on.update('secret', 
                when=kopf.any_([
                    namespace_inclusion,
                    get_annotation,
                    ])
                )
def update_fn(memo: kopf.Memo, name, body, logger, **_):

    result = aws_secrets_manager.update_secret(name)
    logger.info(f"Config: {memo.global_config}")
    logger.info(f"Result: {result}")
    logger.info(f"Secret: {body}")
