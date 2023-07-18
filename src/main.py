import kopf
from providers import aws_secrets_manager
from config import load_config

# Conditional checks for namespace and annotation

def namespace_inclusion(namespace, memo: kopf.Memo, **_): 

    if namespace in memo.global_config["kubernetes"]["excluded_namespaces"]:
        return False
    
    if len(memo.global_config["kubernetes"]["included_namespaces"]) == 0:
        return True
    
    if namespace in memo.global_config["kubernetes"]["included_namespaces"]:
        return True

def get_annotation(annotations, **_): return annotations.get('dom.dev/distribute') == 'true'

# Setup config loading

@kopf.on.startup()
def start_background_worker(memo: kopf.Memo, logger, **_):
    memo.global_config = load_config()

# Run external secret creation on creation of new k8s secret
# Only if namespace is whitelisted and/or annotation is present

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

# Run external secret creation on update of k8s secret
# Only if namespace is whitelisted and/or annotation is present

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

# Reconcile secrets in cluster
# Only if namespace is whitelisted and/or annotation is present

@kopf.timer('secret', 
                when=kopf.any_([
                    namespace_inclusion,
                    get_annotation,
                    ]), 
            interval=60, 
            initial_delay=30)
def check_fn(memo: kopf.Memo, logger, **_):
    logger.info(f"Starting Reconciliation")
