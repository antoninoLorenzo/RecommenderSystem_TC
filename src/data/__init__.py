"""
Utilities for data package
"""
import os
import sys
import inspect
import functools
from abc import ABC

# --- Try imports
try:
    from pandas import DataFrame, read_sql_query
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session, sessionmaker
    from sqlalchemy.exc import SQLAlchemyError
except ImportError as import_err:
    print(f'[!] {import_err}')
    sys.exit(1)

from src import singleton

# --- Try build database connection link
try:
    """
    DB_LINK = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
        os.environ["DB_USR"],
        os.environ["DB_PSW"],
        os.environ["DB_HOST"],
        os.environ["DB_PORT"],
        os.environ["DB_CONN"]
    )
    """
    DB_LINK = 'mysql+pymysql://root:1234@localhost:3306/turing_careers'
except KeyError as env_not_found:
    print(f'[!] Environment Variable Not Found : {env_not_found}')
    sys.exit(1)


def not_none(*param_names):
    """
    Decorator used to check that during initialization of object specified parameters are not none.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            bound_args = inspect.signature(func).bind(*args, **kwargs).arguments
            for param_name in param_names:
                if param_name in bound_args and bound_args[param_name] is None:
                    raise ValueError(f"Parameter '{param_name}' cannot be None")
            return func(*args, **kwargs)
        return wrapper
    return decorator


class Item(ABC):
    """
    Interface for Developers and Offers
    """
    pass


@singleton
class DatabaseEngineFactory:
    """
    Initialized at system startup, is used to share a session factory between all threads.
    """

    def __init__(self):
        try:
            self.__create_engine = create_engine(DB_LINK)
        except SQLAlchemyError as alchemy_err:
            print(f'[!] {alchemy_err}')
        self.__session_factory = sessionmaker(bind=self.__create_engine)

    def get_instance(*args, **kwargs):
        raise NotImplementedError()

    @property
    def session(self):
        return self.__session_factory()
