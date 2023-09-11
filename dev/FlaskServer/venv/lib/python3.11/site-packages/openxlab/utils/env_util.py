import os


def get_env(env_name) -> str:
    return os.environ.get(env_name)


def set_env(env_name, env_value):
    os.environ[env_name] = env_value
