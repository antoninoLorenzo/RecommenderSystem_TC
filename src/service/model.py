"""
Model Component is the Core of the Recommender Algorithm; exposes recommendation functionality.
ModelManager should be used to interact with OfferModel and DeveloperModel, all necessary methods
to interact with those are specified in Model interface.
"""
from abc import ABC, abstractmethod

from pandas import DataFrame
from sklearn.cluster import Birch
from sklearn.decomposition import PCA

from src.data import Item


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

        """

    @abstractmethod
    def update_item(self, item: Item):
        """

        """

    @abstractmethod
    def remove_item(self, item: Item):
        """
        """


class ModelManager:
    """

    """
    def get_offers_model(self) -> Model:
        pass

    def get_developers_model(self) -> Model:
        pass


class OfferModel(Model):
    """
    Contains a Similarity Based model to recommend Offers to Developers.
    """
    def __init__(self):
        # --- load offers in dataframe
        self.__offers = DataFrame()

        # --- model first train
        self.__model = Birch()
        self.__reducer = PCA(2)

    def similar_items(self, item: Item) -> list[Item]:
        raise NotImplementedError()

    def add_item(self, item: Item):
        raise NotImplementedError()

    def update_item(self, item: Item):
        raise NotImplementedError()

    def remove_item(self, item: Item):
        raise NotImplementedError()


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

    def similar_items(self, item: Item) -> list[Item]:
        raise NotImplementedError()

    def add_item(self, item: Item):
        raise NotImplementedError()

    def update_item(self, item: Item):
        raise NotImplementedError()

    def remove_item(self, item: Item):
        raise NotImplementedError()

