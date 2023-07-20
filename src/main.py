"""
Main operator logic
"""

import kopf
from src.providers import aws_secrets_manager
from src.config import ConfigLoader
from src.utils import reconciliation


def namespace_inclusion(namespace, memo: kopf.Memo, **_):
    """
    Conditional checks for namespace
    """
    conditional = False
    if namespace in memo.global_config["kubernetes"]["excluded_namespaces"]:
        conditional = False
    if len(memo.global_config["kubernetes"]["included_namespaces"]) == 0:
        conditional = True
    if namespace in memo.global_config["kubernetes"]["included_namespaces"]:
        conditional = True
    return conditional


def get_annotation(
        annotations,
        **_):
    """
    Conditional check for annotation
    """
    return annotations.get('dom.dev/distribute') == 'true'


@kopf.on.startup()
def start_background_worker(memo: kopf.Memo, logger, **_):
    """
    Setup config loading
    """
    logger.info("Starting up")
    config_loader = ConfigLoader()
    memo.global_config = config_loader.load_config()
    logger.info(f"Config Loaded: {memo.global_config}")


@kopf.on.create('secret',
                when=kopf.any_([
                    namespace_inclusion,
                    get_annotation,
                ])
                )
def create_fn(memo: kopf.Memo, name, body, logger, **_):
    """
    Run external secret creation on creation of new k8s secret
    Only if namespace is whitelisted and/or annotation is present
    """
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
    """
    Run external secret creation on update of k8s secret
    Only if namespace is whitelisted and/or annotation is present
    """
    result = aws_secrets_manager.update_secret(name)
    logger.info(f"Config: {memo.global_config}")
    logger.info(f"Result: {result}")
    logger.info(f"Secret: {body}")


@kopf.timer('secret',
            when=kopf.any_([
                namespace_inclusion,
                get_annotation,
            ]),
            interval=60,
            initial_delay=30,
            idle=60)
def check_fn(name, logger, **_):
    """
    Reconcile secrets in cluster
    Only if namespace is whitelisted and/or annotation is present
    """
    logger.info("Starting Reconciliation")
    should_reconcile = aws_secrets_manager.check_secret(
        client=None, secret_name=name)
    if isinstance(should_reconcile) is int:
        logger.info(
            reconciliation.reconcile_secret(
                secret_name=name,
                age=should_reconcile))
    else:
        logger.error(should_reconcile)
