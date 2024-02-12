"""
Model Component is the Core of the Recommender Algorithm; exposes recommendation functionality.
ModelManager should be used to interact with OfferModel and DeveloperModel, all necessary methods
to interact with those are specified in Model interface.
"""
import sys
from collections import Counter
from abc import ABC, abstractmethod

try:
    from pandas import DataFrame
    from sklearn.cluster import Birch
    from sklearn.decomposition import PCA
except ImportError as import_err:
    print(f'[!] {import_err}')
    sys.exit(1)

from src import singleton
from src.data import Item
from src.data.entity import Developer, Offer, Skill, Language, Location
from src.data.repository import DeveloperRepository, OfferRepository, SkillRepository
from src.logic.distance_matrix import DistanceMatrix, get_offers_frame, get_developers_frame


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

    def __init__(self):
        try:
            print('[i] Initializing OfferModel')
            self.__offers: list[Offer] = OfferRepository().get_offers()
            self.__frame: DataFrame = get_offers_frame(self.__offers)

            print('[i] Building DistanceMatrix')
            self.__matrix = DistanceMatrix(
                self.__frame,
                'RequiredSkills'
            )

            print('[i] Training BIRCH')
            self.__model = Birch(branching_factor=50, n_clusters=3, threshold=0.7)
            self.__reducer = PCA(2)
            self.__reduced_matrix = self.__reducer.fit_transform(self.__matrix.matrix)
            self.__model.fit(self.__reduced_matrix)
            self.__group_labels = self.__model.labels_
            self.__frame['Group'] = self.__group_labels
        except Exception as err:
            print(f'[!] Error initializing OfferModel\n{err}')
            sys.exit(1)
        print('[i] Offer model successfully initialized')

    def get_instance(*args, **kwargs):
        """
        Overwritten by singleton Decorator.
        """
        raise NotImplementedError()

    def similar_items(self, item: Item) -> list[Item]:
        """
        :param item: the developer making the request
        """
        if not isinstance(item, Developer):
            raise ValueError("[OfferModel] similar_items expects a Developer")

        # Step 1: Get Nearest Offers to Developer
        skill_set = {s.name for s in item.skills}
        distances = []
        for offer in self.__offers:
            distances.append({
                'id': offer.id,
                'distance': DistanceMatrix.jaccard(
                    {s.name for s in offer.skills},
                    skill_set
                )
            })

        most_similar_offers = []
        for similarity in [0.1, 0.2, 0.8]:
            [most_similar_offers.append(offer['id']) for offer in distances if offer['distance'] < similarity]
            if len(most_similar_offers) != 0:
                break

        if len(most_similar_offers) == 0:
            return []

        # Step 2: Get Developer Group
        groups = self.__frame.iloc[most_similar_offers]['Group'].tolist()
        group_counts = Counter(groups)
        dev_group = group_counts.most_common(1)[0][0]

        # Step 3: Get most similar offers in group
        group_ids = self.__frame[self.__frame['Group'] == dev_group]['id'].tolist()
        offers = [offer['id'] for offer in distances if offer['distance'] < 0.7 and offer['id'] in group_ids]
        return [o for o in self.__offers if o.id in offers]

    def add_item(self, item: Item):
        if not isinstance(item, Offer):
            raise ValueError("[OfferModel] add_item expects an offer")

    def update_item(self, item: Item):
        if not isinstance(item, Offer):
            raise ValueError("[OfferModel] update_item expects an offer")

    def remove_item(self, item: Item):
        if not isinstance(item, Offer):
            raise ValueError("[OfferModel] remove_item expects an offer")


@singleton
class DeveloperModel(Model):
    """
    Contains a Similarity Based model to recommend Developers to Employers.
    """

    def __init__(self):
        try:
            print('[i] Initializing DeveloperModel')
            self.__developers = DeveloperRepository().get_developers()
            self.__frame = get_developers_frame(self.__developers)

            print('[i] Building DistanceMatrix')
            self.__matrix = DistanceMatrix(
                self.__frame,
                'Skills'
            )

            print('[i] Training BIRCH')
            self.__model = Birch(branching_factor=50, n_clusters=3, threshold=0.5)
            self.__reducer = PCA(2)
            self.__reduced_matrix = self.__reducer.fit_transform(self.__matrix.matrix)
            self.__model.fit(self.__reduced_matrix)
            self.__group_labels = self.__model.labels_
            self.__frame['Group'] = self.__group_labels
        except Exception as err:
            print(f'[!] Error initializing DeveloperModel\n{err}')
            sys.exit(1)
        print('[i] Developer model successfully initialized')

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

if __name__ == "__main__":
    stub_developer = Developer(1, 'Antonino', 'Lorenzo', 'bio',
                               'anton@asd.com', 'DioCiao0003', [Language(1, 'it')],
                               Location(1, 'Avellino', 83.0, 100.0),
                               [Skill(1, 'Java', 'Programming Language')]
                               )

    offer_model: OfferModel = OfferModel()

    output = offer_model.similar_items(stub_developer)
    for out in output:
        print(out, end='\n\n')