from abc import ABC, abstractmethod

import numpy as np
import pandas as pd

from src.data import Item


class DistanceMatrix:

    def __init__(self, frame: pd.DataFrame, column_label: str) -> None:
        """
        :param frame:
        :param column_label:
        """
        self.__distance_matrix = {}

        frame_data = frame[column_label].to_dict()
        for item_id, item_data in frame_data.items():
            if not isinstance(item_data, set):
                raise ValueError('[!] DistanceMatrix: specified column of frame should contains sets')

            distances = []
            for other_item_id, other_item_data in frame_data.items():
                if item_id != other_item_id:
                    distances.append(
                        self.__jaccard(
                            item_data,
                            other_item_data
                        )
                    )
                else:
                    distances.append(0)

            self.__distance_matrix[item_id] = distances

    def add_row(self, new_row: Item):
        pass

    def delete_row(self, row: Item):
        pass

    @property
    def matrix(self):
        return np.array(list(self.__distance_matrix.values()))

    @staticmethod
    def __jaccard(s1: set, s2: set):
        """
        :return: distance between two item-sets
        """
        return 1 - (len(s1.intersection(s2)) / len(s1.union(s2)))


if __name__ == "__main__":
    # --- Get Offers Dataframe
    import sqlite3

    with sqlite3.connect('../../demo/datasets/offers_full.db') as offers_conn:
        offers_frame = pd.read_sql_query('SELECT * FROM offers', offers_conn)


    def string_to_set(item_set):
        return set(item_set.split(', '))


    offers_frame['RequiredSkills'] = offers_frame['RequiredSkills'].apply(string_to_set)

    # Core
    distance_matrix = DistanceMatrix(offers_frame, 'RequiredSkills')

    # --- Test with Birch
    from sklearn.cluster import Birch
    from sklearn.decomposition import PCA
    from sklearn.model_selection import GridSearchCV
    from sklearn.metrics import silhouette_score


    def birch_silhouette_scorer(model, data):
        tmp_labels = model.fit_predict(data)
        score = silhouette_score(data, tmp_labels)
        return score


    param_grid = {
        'n_clusters': [3, 4, 5, 6],
        'threshold': [0.5, 0.7, 0.8],
        'branching_factor': [50, 100]
    }

    _pca = PCA(2)
    _data = _pca.fit_transform(distance_matrix.matrix)
    gsearch_pca = GridSearchCV(Birch(), param_grid, cv=5, scoring=birch_silhouette_scorer, n_jobs=-1)
    gsearch_pca.fit(_data)

    print(f"Best Parameters: {gsearch_pca.best_params_}")
    print(f"Best Silhouette Score: {gsearch_pca.best_score_:.2f}")

