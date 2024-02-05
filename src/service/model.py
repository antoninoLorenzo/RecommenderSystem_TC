"""
Model Component is the Core of the Recommender Algorithm; exposes recommendation functionality.
ModelManager should be used to interact with OfferModel and DeveloperModel, all necessary methods
to interact with those are specified in Model interface.
"""
import sys
from abc import ABC, abstractmethod

try:
    from pandas import DataFrame
    from sklearn.cluster import Birch
    from sklearn.decomposition import PCA
except ImportError as import_err:
    print(f'[!] {import_err}')
    sys.exit(1)

from src.data import Item


def singleton(cls):
    """
    Decorator for OfferModel and DeveloperModel, those should be initialized only once.
    """
    instances = {}

    class SingletonWrapper(cls):
        @staticmethod
        def get_instance(*args, **kwargs):
            """
            Overwrite models get_instance method to implement Singleton
            """
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
            return instances[cls]

    return SingletonWrapper


class Model(ABC):
    """
    Interface for OfferModel and Developer Model.
    """

    @abstractmethod
    def similar_items(self, item: Item) -> list[Item]:
        """
        :param item: Item Type A
        :return: list[Item Type B]
        """

    @abstractmethod
    def add_item(self, item: Item):
        """
        :param item: should be the same type of model items and shouldn't be present in model
        """

    @abstractmethod
    def update_item(self, item: Item):
        """
        :param item: should be the same type of model items and item should be present in model
        """

    @abstractmethod
    def remove_item(self, item: Item):
        """
        :param item: should be the same type of model items and item should be present in model
        """


class ModelManager:
    """
    Static class used to access Models
    """

    @staticmethod
    def get_offers_model(*args, **kwargs) -> Model:
        """
        :return : new OfferModel or current instance
        """
        ModelManager.__offer_model = OfferModel.get_instance(*args, **kwargs)
        return ModelManager.__offer_model

    @staticmethod
    def get_developers_model(*args, **kwargs) -> Model:
        """
        :return : new DeveloperModel or current instance
        """
        ModelManager.__offer_model = OfferModel.get_instance(*args, **kwargs)
        return ModelManager.__offer_model


@singleton
class OfferModel(Model):
    """
    Contains a Similarity Based model to recommend Offers to Developers.
    """

    def __init__(self, value):
        self.a = value
        # --- load offers in dataframe
        # self.__offers = DataFrame()

        # --- model first train
        # self.__model = Birch()
        # self.__reducer = PCA(2)

    def get_instance(*args, **kwargs):
        """
        Overwritten by singleton Decorator.
        """
        raise NotImplementedError()

    def similar_items(self, item: Item) -> list[Item]:
        raise NotImplementedError()

    def add_item(self, item: Item):
        raise NotImplementedError()

    def update_item(self, item: Item):
        raise NotImplementedError()

    def remove_item(self, item: Item):
        raise NotImplementedError()


@singleton
class DeveloperModel(Model):
    """
    Contains a Similarity Based model to recommend Developers to Employers.
    """

    def __init__(self):
        # --- load developers in dataframe
        self.__developers = DataFrame()

        # --- model first train
        self.__model = Birch()
        self.__reducer = PCA(2)

    def get_instance(*args, **kwargs):
        """
        Overwritten by singleton Decorator.
        """
        raise NotImplementedError()

    def similar_items(self, item: Item) -> list[Item]:
        raise NotImplementedError()

    def add_item(self, item: Item):
        raise NotImplementedError()

    def update_item(self, item: Item):
        raise NotImplementedError()

    def remove_item(self, item: Item):
        raise NotImplementedError()


# --- Development Only

def is_singleton():
    """."""
    offer_model = ModelManager.get_offers_model(2)
    print(f'first instance a: {offer_model.a}')
    offer_model.a = 4
    print(f'first instance a: {offer_model.a}')
    new_instance = ModelManager.get_offers_model()
    print(f'other instance a: {new_instance.a}')


if __name__ == "__main__":
    is_singleton()
