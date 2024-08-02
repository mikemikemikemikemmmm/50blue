from src.setting.index import get_settings


def is_dev_environment():
    return get_settings().ENVIRONMENT == "dev"


def get_environment():
    return get_settings().ENVIRONMENT
