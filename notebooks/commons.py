"""
Collection of the functions used in analysis and modeling notebooks
"""
from string import punctuation
from functools import lru_cache
from math import radians, cos, sin, asin, sqrt

import requests
import numpy as np
import pandas as pd
from pandas import Series
from sklearn.cluster import KMeans
from scipy.spatial.distance import euclidean
from requests import Response


# --- Modeling
def _jaccard(s1: set, s2: set):
    """
    :return: distance between two item-sets
    """
    return 1 - (len(s1.intersection(s2)) / len(s1.union(s2)))


def get_distance_matrix(frame: pd.DataFrame, col_name: str):
    """
    Computes distance matrix between items in a pandas DataFrame using Jaccard Distance.
    The feature given as *col_name* should contain item-sets as Python set().
    :param frame: original dataset
    :param col_name: feature containing item-sets
    """
    distances = []
    for i, row1 in frame.iterrows():
        distances.append([])
        for j, row2 in frame.iterrows():
            if i != j:
                distances[-1].append(_jaccard(row1[col_name], row2[col_name]))
            else:
                distances[-1].append(0)
    return pd.DataFrame(distances, index=frame.index, columns=frame.index)


def _item_cluster_distance(frame: pd.DataFrame, item: Series, target: int,
                           group_label: str = 'Group',
                           distance_label: str = 'RequiredSkills'):
    """
    Used to compute silhouette score.
    Computes distance between an item in a cluster X and the other items in a cluster Y.
    Used also when X and Y are the same clusters.
    :param target: target cluster group label
    :param group_label: frame column label for the cluster group label
    """
    group = frame[frame[group_label] == target]
    den = len(list(group.index))
    distance = 0

    for it in group.iterrows():
        if not it[1].equals(item):
            distance += _jaccard(item[distance_label], it[1][distance_label])
    if distance == 0:
        distance = 1
    if den == 0:
        den = 1
    try:
        return distance / den
    except ZeroDivisionError:
        return 0


def _find_nearest_cluster(centroids, target_label: int):
    """
    Used to compute silhouette score.
    """
    nearest = None
    target_centroid = centroids.iloc[target_label]
    min_dist = float('inf')

    for label, vector in centroids[centroids.index != target_label].iterrows():
        dist = euclidean(target_centroid, vector)
        if dist < min_dist:
            min_dist = dist
            nearest = label

    return nearest


def kmeans_silhouette(frame: pd.DataFrame,
                      clustering: KMeans,
                      group_label: str = 'Group',
                      distance_label: str = 'RequiredSkills'):
    """
    ...
    """
    silhouette_scores = []
    # basically for each cluster group (0, 1, 2, ...)
    for target_cluster in list(np.unique(frame[group_label])):
        nearest_cluster = _find_nearest_cluster(
            pd.DataFrame(clustering.cluster_centers_),
            target_cluster
        )
        for _, item in frame.iterrows():
            a = _item_cluster_distance(frame, item, target_cluster, group_label, distance_label)
            b = _item_cluster_distance(frame, item, nearest_cluster, group_label, distance_label)
            silhouette_score = (b - a) / max(a, b)
            silhouette_scores.append(silhouette_score)

    return np.mean(silhouette_scores)


def _similar_offers_with_cluster(frame: pd.DataFrame, offer_id: int) -> list:
    target_group = frame.loc[offer_id, 'Group']
    return list(
        frame[
            frame['Group'] == target_group
        ].index
    )


def similar_offers_with_cluster(frame: pd.DataFrame, offer_id: int) -> list:
    return [frame.iloc[oid] for oid in _similar_offers_with_cluster(offer_id)]


# --- Text parsing
punct = list(punctuation)
punct.remove('+')
punct.remove('#')

REMOVAL = {p: ' ' for p in punct}
REMOVAL['\n'] = ' '
REMOVAL['/'] = ' '
REMOVAL['('] = ' '
REMOVAL[')'] = ' '
REMOVAL[','] = ' '
REMOVAL['>'] = ' '
REMOVAL['.'] = ' .'


def remove_symbols(content: str, remove_map=None) -> str:
    """
    Replace a symbol (character or string) in *content* using a remove_map, default is REMOVAL
    :param content: textual data
    :param remove_map: {symbol: replacement}, default is REMOVAL
    """
    if remove_map is None:
        remove_map = REMOVAL
    for old, new in remove_map.items():
        content = content.replace(old, new)
    return content.lower()


def extract_symbols(content: str, available_symbols: list) -> set:
    """
    Extract given symbols from content
    :param content: textual data
    :param available_symbols: list containing symbols to extract
    """
    s = set()
    prev = ''
    for word in content.split():
        if word in available_symbols:
            s.add(word)
        elif f'{prev} {word}' in available_symbols:
            s.add(f'{prev} {word}')
        prev = word
    return s


# --- Skill Utils

def translate_skills(skills: set, skills_frame, to_id=False) -> set:
    """
    Internally calls id_to_skill or skill_to_id
    """
    if to_id:
        return skill_to_id(skills, skills_frame)
    return id_to_skill(skills, skills_frame)


def id_to_skill(skills: set[int], skills_frame) -> set[str]:
    """
    Converts skills in a set of skills from id to skill
    """
    int_ids = {int(item) for item in skills}

    out = set()
    for skill in int_ids:
        try:
            out.add(skills_frame.loc[skill, 'SKILL'])
        except KeyError:
            pass

    return out


def skill_to_id(skills: set[str], skills_frame) -> set[int]:
    """
    Converts skills in a set of skills from skill to id
    """
    out = set()
    for skill in skills:
        tmp = list(skills_frame.loc[skills_frame['SKILL'].apply(lambda val: val.lower()) == skill.lower()].index)
        out.add(tmp[0])

    return out


# --- Location Utils

PLACES_API = '''https://maps.googleapis.com/maps/api/place/textsearch/json?query={}&key=AIzaSyBg32OrPVN2Qi1q6hJq16EagNSiwW4O6ys&language=it'''


@lru_cache()
def get_coordinates(location: str) -> dict:
    """
    Make a request to Google Places API to get Longitude and Latitude for a location string.
    """
    response: Response = requests.get(PLACES_API.format(location), timeout=10)
    return response.json()['results'][0]['geometry']['location']


def haversine(lon1, lat1, lon2, lat2):
    """
    Prompt-Engineering basatissimo.
    Calcola la distanza fra due posti utilizzando le coordinate e tenendo presente
    cose che onestamente non mi sono molto chiare
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    r = 6371
    return c * r


def location_distance(frame: pd.DataFrame, off1_id, off2_id, location_column='Location') -> float:
    """
    Find distance between two locations in a dataframe.
    """
    loc1 = frame.loc[off1_id, location_column]
    loc2 = frame.loc[off2_id, location_column]

    lat1, lon1 = get_coordinates(loc1).values()
    lat2, lon2 = get_coordinates(loc2).values()

    return haversine(lon1, lat1, lon2, lat2)


def get_near_offers(frame: pd.DataFrame, location: str, max_distance: float = 500):
    """
    Gets a location string as input and returns pandas Indexes used to filter a Dataframe:
    1. calls get_coordinates to get latitude and longitude;
    2. computes distance from query location and an offer;
    3. sort distances and filter by max_distance.
    """
    user_lat, user_lon = get_coordinates(location).values()
    distances: pd.Series = frame.apply(
        lambda offer: haversine(
            user_lon, user_lat,
            offer['Longitude'], offer['Latitude']
        )
        , axis=1
    ).rename('Distance').sort_values()
    return list(distances[distances < max_distance].index)
