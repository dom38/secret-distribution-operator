import yaml

CONFIG = None

def load_config():
    global CONFIG
    if CONFIG is None:
        with open('config/config.yaml', 'r') as file:
            CONFIG = yaml.safe_load(file)
    return CONFIG
