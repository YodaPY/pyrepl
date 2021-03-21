import os

def get_config_path() -> str:
    home = os.path.expanduser("~")
    config_path = os.path.join(home, ".config/pyrepl")

    return config_path