"""
Utilities for whole project
"""

def singleton(cls):
    """
    Decorator Singleton Design Pattern applied on classes.
    """
    instances = {}

    class SingletonWrapper(cls):
        @staticmethod
        def get_instance(*args, **kwargs):
            """
            Overwrite get_instance method to implement Singleton
            """
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
            return instances[cls]

    return SingletonWrapper
