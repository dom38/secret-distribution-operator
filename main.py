import kopf
import os
import kubernetes
import yaml
import json

@kopf.on.create('secret')
def create_fn(name, meta, namespace, logger, **kwargs):
    path = os.path.join(os.path.dirname(__file__), 'resources/distributed-secret.yaml')
    template = open(path, 'rt').read()
    text = template.format(name=name, labels=meta.labels)
    data = yaml.safe_load(text)

    api = kubernetes.client.CustomObjectsApi()
    obj = api.create_namespaced_custom_object(
        namespace=namespace,
        body=data,
        group="dom.dev",
        version="v1",
        plural="distributedsecrets",
    )

    logger.info(f"distributed-secret created: {json.dumps(obj, indent=4)}")

@kopf.on.update('secret')
def update_fn(meta, body, namespace, logger, **kwargs):

    logger.info(f"distributed-secret status: {body}")
    secret_name = meta["name"]
    secret_patch = {'data': body["data"], 'metadata': {'labels': meta.labels}}

    api = kubernetes.client.CustomObjectsApi()
    obj = api.patch_namespaced_custom_object(
        namespace=namespace,
        group="dom.dev",
        version="v1",
        plural="distributedsecrets",
        name=secret_name,
        body=secret_patch,
    )

    logger.info(f"distributed-secret updated: {json.dumps(obj, indent=4)}")
