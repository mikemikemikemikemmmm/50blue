from functools import lru_cache

from src.models.drink import DrinkModel
from src.models.topping import ToppingModel
from src.setting.index import get_settings
from src.db.engine import get_db

def is_dev_environment():
    return get_settings().ENVIRONMENT == "dev"

def get_environment():
    return get_settings().ENVIRONMENT


@lru_cache()
def get_all_drink():
    session = get_db().__next__()
    all_drink = session.query(DrinkModel).all()
    session.close()
    return all_drink


