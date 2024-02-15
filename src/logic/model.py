"""
Model Component is the Core of the Recommender Algorithm; exposes recommendation functionality.
ModelManager should be used to interact with OfferModel and DeveloperModel, all necessary methods
to interact with those are specified in Model interface.
"""
import sys
import time
from collections import Counter
from abc import ABC, abstractmethod

try:
    import numpy as np
    from pandas import DataFrame, concat, Series
    from sklearn.cluster import Birch
    from sklearn.decomposition import PCA
except ImportError as import_err:
    print(f'[!] {import_err}')
    sys.exit(1)

from src import singleton
from src.data import *
from src.data.entity import *
from src.data.repository import *


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
        ModelManager.__developer_model = DeveloperModel.get_instance(*args, **kwargs)
        return ModelManager.__developer_model


class ItemDistance:
    __slot__ = ('__item_id', '__item_distance')

    def __init__(self, item_id, item_distance):
        self.__item_id = item_id
        self.__item_distance = item_distance

    @property
    def item_id(self):
        return self.__item_id

    @property
    def item_distance(self):
        return self.__item_distance


class DistanceMatrix:
    """
    Distance Matrix computes distances between items in a dataset.
    Internally uses Jaccard distance, so Items must contain a set feature.
    """

    def __init__(self, frame: DataFrame, column_label: str) -> None:
        """
        :param frame: dataset.
        :param column_label: label of feature X of dataset represented as a set.
        """
        self.__distance_matrix = {}
        self.__size = len(frame)
        frame_data = frame[column_label].to_dict()
        self.__frame_data = frame_data

        for item_id, item_data in frame_data.items():
            if not isinstance(item_data, set):
                raise ValueError('[!] DistanceMatrix: specified column of frame should contains sets')

            distances = []
            for other_item_id, other_item_data in frame_data.items():
                if item_id != other_item_id:
                    distances.append(ItemDistance(other_item_id, self.jaccard(item_data, other_item_data)))
                    # distances.append(self.jaccard(item_data, other_item_data))
                else:
                    # distances.append((item_id, 0))
                    distances.append(ItemDistance(item_id, 0))

            self.__distance_matrix[item_id] = distances

    def get_item(self, item_id):
        for key, value in self.__frame_data.items():
            if key == item_id:
                return value
        return None

    def add_item(self, new_item: Item):
        """
        Internally computes distances between new_item and stored items.
        """
        if isinstance(new_item, Developer):
            item: Developer = new_item
        elif isinstance(new_item, Offer):
            item: Offer = new_item
        else:
            raise ValueError('[!] DistanceMatrix: add_item requires Offer or Developer')

        distances = []
        skills = set([skill.name for skill in item.skills])
        for item_id, item_data in self.__frame_data.items():
            d = self.jaccard(item_data, skills)
            distance = ItemDistance(item_id, d)
            distance_col = ItemDistance(item.id, d)
            distances.append(distance)
            self.__distance_matrix[item_id].append(distance_col)

        distances.append(ItemDistance(item.id, 0))
        self.__distance_matrix[item.id] = distances
        self.__frame_data[item.id] = skills
        self.__size += 1

    def delete_item(self, to_delete: Item):
        """
        Removes stored item that must exist in the distance matrix.
        """
        if isinstance(to_delete, Developer):
            item: Developer = to_delete
        elif isinstance(to_delete, Offer):
            item: Offer = to_delete
        else:
            raise ValueError('[!] DistanceMatrix: add_item requires Offer or Developer')

        for key, value in self.__distance_matrix.items():
            if key != item.id:
                for distance in value:
                    if item.id == distance.item_id:
                        value.remove(distance)

        self.__distance_matrix.pop(item.id)
        self.__frame_data.pop(item.id)
        self.__size -= 1

    @property
    def matrix(self):
        """
        Access distance matrix distances as numpy ndarray
        """
        # Previous Version
        # return np.array(list(self.__distance_matrix.values()))
        distances_lists = [[item_distance.item_distance for item_distance in item_distances] for item_distances in
                           self.__distance_matrix.values()]
        return np.array(distances_lists)

    @property
    def size(self):
        return self.__size

    @staticmethod
    def jaccard(s1: set, s2: set):
        """
        :return: distance between two item-sets
        """
        return 1 - (len(s1.intersection(s2)) / len(s1.union(s2)))



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
        max_similarity = 0
        similarity_dict = {0.1: 0.6, 0.2: 0.7, 0.8: 0.9}
        for similarity in [0.1, 0.2, 0.8]:
            [most_similar_offers.append(offer['id']) for offer in distances if offer['distance'] < similarity]
            if len(most_similar_offers) != 0:
                max_similarity = similarity

        if len(most_similar_offers) == 0:
            return []

        # Step 2: Get Developer Group
        groups = self.__frame.iloc[most_similar_offers]['Group'].tolist()
        group_counts = Counter(groups)
        dev_group = group_counts.most_common(1)[0][0]

        # Step 3: Get most similar offers in group
        group_ids = self.__frame[self.__frame['Group'] == dev_group]['id'].tolist()
        offers = [offer['id'] for offer in distances if offer['distance'] <= similarity_dict[max_similarity] and offer['id'] in group_ids]
        return [o for o in self.__offers if o.id in offers]

    def add_item(self, item: Item):
        if not isinstance(item, Offer):
            raise ValueError("[OfferModel] add_item expects an offer")
        try:
            self.__matrix.add_item(item)
            self.__reduced_matrix = self.__reducer.fit_transform(self.__matrix.matrix)
            self.__model.fit(self.__reduced_matrix)
            self.__group_labels = self.__model.labels_
            unique_skills = {s.name for s in item.skills}
            frame_row = DataFrame({
                'id': item.id,
                'Title': item.title,
                'RequiredSkills': [list(unique_skills)],
                'Group': -1
            }) # TODO: add all fields
            self.__frame = concat([self.__frame, frame_row], ignore_index=False)
            self.__frame['Group'] = self.__group_labels
        except Exception as err:
            print('[!] Failed adding Offer')
            raise ValueError("Couldn't add Item")

    def update_item(self, item: Item):
        if not isinstance(item, Offer):
            raise ValueError("[OfferModel] update_item expects an offer")
        try:
            self.remove_item(item)
            self.add_item(item)
        except Exception as err:
            print('[!] Failed updating item')

    def remove_item(self, item: Item):
        if not isinstance(item, Offer):
            raise ValueError("[OfferModel] remove_item expects an offer")

        try:
            self.__matrix.delete_item(item)
            self.__reduced_matrix = self.__reducer.fit_transform(self.__matrix.matrix)
            self.__model.fit(self.__reduced_matrix)
            self.__group_labels = self.__model.labels_
            self.__frame = self.__frame[self.__frame['id'] != item.id]
            self.__frame['Group'] = self.__group_labels
        except Exception as err:
            print('[!] Failed removing Offer')
            raise ValueError("Couldn't remove item")

    def get_item(self, item_id):
        return self.__frame[self.__frame['id'] == item_id]


@singleton
class DeveloperModel(Model):
    """
    Contains a Similarity Based model to recommend Developers to Employers.
    # TODO: check if works after copying all from OfferModel
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
        if not isinstance(item, Offer):
            raise ValueError("[DeveloperModel] similar_items expects an Offer")

        # Step 1: Get Nearest Offers to Developer
        skill_set = {s.name for s in item.skills}
        distances = []
        for dev in self.__developers:
            distances.append({
                'id': dev.developer_id,
                'distance': DistanceMatrix.jaccard(
                    {s.name for s in dev.skills},
                    skill_set
                )
            })

        most_similar_devs = []
        max_similarity = 0
        similarity_dict = {0.1: 0.6, 0.2: 0.7, 0.8: 0.9}
        for similarity in [0.1, 0.2, 0.8]:
            for developer in distances:
                if developer['distance'] < similarity:
                    most_similar_devs.append(developer['id'].tolist()[0])
            if len(most_similar_devs) != 0:
                max_similarity = similarity
                break

        if len(most_similar_devs) == 0:
            return []

        # Step 2: Get Developer Group
        groups = self.__frame.iloc[most_similar_devs]['Group'].tolist()
        group_counts = Counter(groups)
        offer_group = group_counts.most_common(1)[0][0]

        # Step 3: Get most similar offers in group
        ids = self.__frame[self.__frame['Group'] == offer_group]['id'].tolist()
        group_ids = [i.tolist()[0] for i in ids]

        tmp_developers = []
        for developer in distances:
            if developer['distance'] < similarity_dict[max_similarity]:
                if developer['id'].tolist()[0] in group_ids or len(tmp_developers) < 2:
                    tmp_developers.append(developer)

        developer_ids = []
        for t in tmp_developers:
            for v in t.values():
                if isinstance(v, Series):
                    developer_ids.append(v.tolist()[0])

        output = set()
        for out in self.__developers:
            _id = out.developer_id.tolist()[0]
            if _id in developer_ids:
                output.add(out)

        return list(output)

    def add_item(self, item: Item):
        if not isinstance(item, Developer):
            raise ValueError("[DeveloperModel] add_item expects a developer")
        try:
            self.__matrix.add_item(item)
            self.__reduced_matrix = self.__reducer.fit_transform(self.__matrix.matrix)
            self.__model.fit(self.__reduced_matrix)
            self.__group_labels = self.__model.labels_
            unique_skills = {s.name for s in item.skills}
            frame_row = DataFrame({
                'id': item.developer_id,
                'SkillsSkills': [list(unique_skills)],
                'Group': -1
            }) # TODO: add all fields
            self.__frame = concat([self.__frame, frame_row], ignore_index=False)
            self.__frame['Group'] = self.__group_labels
        except Exception as err:
            print('[!] Failed adding Developer')
            raise ValueError("Couldn't add Item")

    def update_item(self, item: Item):
        if not isinstance(item, Developer):
            raise ValueError("[DeveloperModel] update_item expects a developer")
        try:
            self.remove_item(item)
            self.add_item(item)
        except Exception as err:
            print('[!] Failed updating item')

    def remove_item(self, item: Item):
        if not isinstance(item, Developer):
            raise ValueError("[DeveloperModel] remove_item expects a developer")

        try:
            self.__matrix.delete_item(item)
            self.__reduced_matrix = self.__reducer.fit_transform(self.__matrix.matrix)
            self.__model.fit(self.__reduced_matrix)
            self.__group_labels = self.__model.labels_
            self.__frame = self.__frame[self.__frame['id'] != item.developer_id]
            self.__frame['Group'] = self.__group_labels
        except Exception as err:
            print('[!] Failed removing Developer')
            raise ValueError("Couldn't remove item")

