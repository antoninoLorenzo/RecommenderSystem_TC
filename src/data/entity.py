"""
Contains database Entities
"""
import json

from src.data import Item, not_none


class Skill:
    """
    Skill POPO
    """
    @not_none('id', 'name', 'type')
    def __init__(self,
                 id: int,
                 name: str,
                 type: str):
        self.__id: int = id
        self.__name: str = name
        self.__type: str = type

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def type(self):
        return self.__type


class Location:
    """
    Location POPO
    """

    @not_none('loc_id', 'name', 'latitude', 'longitude')
    def __init__(self, loc_id, name, latitude, longitude):
        self.__id: int = loc_id
        self.__name: str = name
        self.__lat: float = latitude
        self.__lon: float = longitude

    @property
    def location_id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def latitude(self):
        return self.__lat

    @property
    def longitude(self):
        return self.__lon

    def __str__(self):
        return f'[{self.__id}]: {self.__name} ({self.__lat}, {self.__lon})'


class Developer(Item):
    """
    Developer POPO
    """

    @not_none('dev_id', 'f_name', 'l_name', 'bio', 'mail', 'psw', 'location', 'skills')
    def __init__(self, dev_id, f_name, l_name, bio, mail, psw, location, skills):
        self.__id: int = dev_id
        self.__f_name: str = f_name
        self.__l_name: str = l_name
        self.__mail: str = mail
        self.__psw: str = psw
        self.__location: Location = location
        self.__skills: list = skills

    @staticmethod
    def from_dict(data: dict) -> 'Developer':
        """
        Creates a Developer instance from a JSON string.
        """

        dev_id = data['dev_id']
        f_name = data['f_name']
        l_name = data['l_name']
        mail = data['mail']
        psw = data['psw']
        location_data = data['location']
        skills = data['skills']

        location = Location(
            location_data['loc_id'],
            location_data['loc_name'],
            location_data['lat'],
            location_data['lon']
        )

        return Developer(dev_id, f_name, l_name, mail, psw, location, skills)

    def __str__(self):
        return (f'[{self.__id}]: {self.__f_name} {self.__l_name} ({self.__mail}: {self.__psw})\n'
                f'Skills: {self.__skills}\n'
                f'Location: {self.__location}')

    @property
    def developer_id(self):
        return self.__id

    @property
    def first_name(self):
        return self.__f_name

    @property
    def last_name(self):
        return self.__l_name

    @property
    def mail(self):
        return self.__mail

    @property
    def psw(self):
        return self.__psw

    @property
    def location(self):
        return self.__location

    @property
    def skills(self):
        return self.__skills


class Offer(Item):
    """
    Offer POPO
    """
    @not_none('id', 'title', 'state', 'description', 'location_type', 'employer_id', 'skills')
    def __init__(self,
                 id: int,
                 title: str,
                 state: str,
                 description: str,
                 employer_id: int,
                 skills: list[Skill],
                 location_type: str,
                 location: Location = None):
        self.__id: int = id
        self.__title: str = title
        self.__state: str = state
        self.__description: str = description
        self.__location_type: str = location_type
        self.__location = location
        self.__employer_id = employer_id
        self.__skills = skills

    @property
    def id(self):
        return self.__id

    @property
    def title(self):
        return self.__title

    @property
    def state(self):
        return self.__state

    @property
    def description(self):
        return self.__description

    @property
    def location_type(self):
        return self.__location_type

    @property
    def location(self):
        return self.__location

    @property
    def employer_id(self):
        return self.__employer_id

    @property
    def skills(self):
        return self.__skills
