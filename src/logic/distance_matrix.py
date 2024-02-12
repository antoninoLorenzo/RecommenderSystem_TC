"""
This module is for development, once done DistanceMatrix will go in model.py
"""
import sys

import numpy as np
import pandas as pd

from src.data import Item
from src.data.entity import Offer, Developer
from src.data.repository import OfferRepository, DeveloperRepository


class ItemDistance:
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

    def __init__(self, frame: pd.DataFrame, column_label: str) -> None:
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
                    distances.append(ItemDistance(other_item_id, self.jaccard(item_data,other_item_data)))
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
            if key != 1000:
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


def get_offers_frame(offer_list: list[Offer]):
    offers_dict = []
    for o in offer_list:
        skill_set = {s.name for s in o.skills}
        offers_dict.append({
            'id': o.id,
            'Title': o.title,
            'RequiredSkills': skill_set
        })
    return pd.DataFrame(offers_dict)


def get_developers_frame(developer_list: list[Developer]):
    developers_dict = []
    for d in developer_list:
        skills_set = {s.name for s in d.skills}
        developers_dict.append({
            'id': d.developer_id,
            'Skills': skills_set
        })
    return pd.DataFrame(developers_dict)


if __name__ == "__main__":
    # --- Get Offers Dataframe
    offers: list[Offer] = OfferRepository().get_offers()
    distance_matrix = DistanceMatrix(
        get_offers_frame(offers),
        'RequiredSkills'
    )

    from src.presentation import stub_offer
    distance_matrix.add_item(stub_offer)
    s = distance_matrix.get_item(1000)
    print(s)
    distance_matrix.delete_item(stub_offer)
    s = distance_matrix.get_item(1000)
    print(s)