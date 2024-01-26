import time

import numpy as np
import pandas as pd


def _jaccard(s1: set, s2: set):
    return 1 - (len(s1.intersection(s2)) / len(s1.union(s2)))


def test(set1, set2):
    start = time.time()
    out = _jaccard(set1, set2)
    end = time.time()
    print(f'Done in: {(end - start):.4f}s')
    return out


if __name__ == "__main__":

    # --- Distance Matrix representation
    # - in that way items can be accessed with id
    # - matrix can implement update and remove effortless
    # - storing only unique distances is an optimization but conversion must be fixed
    distance_matrix = {
        'element1': {'element2': 12, 'element3': 13},
        'element2': {'element3': 23}, #, 'element1': 12},
        'element3': {}#{'element1': 13, 'element2': 23},
    }

    # --- Convert Distance Matrix to pandas dataframe
    for row, distances in distance_matrix.items():
        distances[row] = 0
        distance_matrix[row] = dict(sorted(distance_matrix[row].items()))

    df = pd.DataFrame.from_dict(distance_matrix, orient='index')
    print(df)