"""
Contains database Entities
"""
from __future__ import annotations
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

    @staticmethod
    def from_list(data: list) -> list[Skill]:
        skills = []
        for skill in data:
            skills.append(Skill(
                id=skill['_Skill__id'],
                name=skill['_Skill__name'],
                type=skill['_Skill__type']
            ))
        return skills

    def to_dict(self):
        return {
            '_Skill__id': self.__id,
            '_Skill__name': self.__name,
            '_Skill__type': self.__type
        }

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def type(self):
        return self.__type


"""
NUKED
class Location:

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
"""


class Language:
    def __init__(self, lid, language_code):
        self.__id = lid
        self.__code = language_code

    @staticmethod
    def from_dict(data: dict) -> Language:
        lid = data['_Language__id']
        code = data['_Language__code']

        return Language(lid, code)

    def to_dict(self):
        return {
            '_Language__id': self.__id,
            '_Language__code': self.__code
        }

    @property
    def code(self):
        return self.__code


class Developer(Item):
    """
    Developer POPO
    """

    @not_none('dev_id', 'f_name', 'l_name', 'bio', 'mail', 'psw', 'languages', 'location', 'skills')
    def __init__(self, dev_id, f_name, l_name, bio, mail, psw, languages, location, skills):
        self.__id: int = dev_id
        self.__f_name: str = f_name
        self.__l_name: str = l_name
        self.__bio: str = bio
        self.__mail: str = mail
        self.__psw: str = psw
        self.__languages: list[Language] = languages
        self.__location: str = location
        self.__skills: list = skills

    @staticmethod
    def from_dict(data: dict) -> 'Developer':
        """
        Creates a Developer instance from a JSON string.
        """

        dev_id = data['_Developer__id']
        f_name = data['_Developer__f_name']
        l_name = data['_Developer__l_name']
        bio = data['_Developer__bio']
        mail = data['_Developer__mail']
        psw = data['_Developer__psw']
        location = data['_Developer__location']

        skills = Skill.from_list(data['_Developer__skills'])

        # location = Location(
        #    location_data['_Location__id'],
        #    location_data['_Location__name'],
        #    location_data['_Location__lat'],
        #    location_data['_Location__lon']
        # )

        language = []

        return Developer(dev_id, f_name, l_name, bio, mail, psw, language, location, skills)

    def __str__(self):
        return (f'[{self.__id}]: {self.__f_name} {self.__l_name} ({self.__mail}: {self.__psw})\n'
                f'Language: {self.__languages}\n'
                f'Skills: {self.__skills}\n'
                f'Location: {self.__location}\n'
                f'Bio: \n{self.__bio}\n')

    def to_dict(self):
        return {
            '_Developer__id': self.__id,
            '_Developer__f_name': self.__f_name,
            '_Developer__l_name': self.__l_name,
            '_Developer__bio': self.__bio,
            '_Developer__mail': self.__mail,
            '_Developer__psw': self.__psw,
            '_Developer__languages': [lang.to_dict() for lang in self.__languages],
            '_Developer__location': self.__location,
            '_Developer__skills': [skill.to_dict() for skill in self.__skills]
        }

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


class Employer:
    def __init__(self, emp_id, f_name, l_name, mail, psw, company_name):
        self.__id: int = emp_id
        self.__f_name: str = f_name
        self.__l_name: str = l_name
        self.__mail: str = mail
        self.__psw: str = psw
        self.__company = company_name

    @staticmethod
    def from_dict(data: dict) -> Employer:
        emp_id = data['_Employer__id']
        f_name = data['_Employer__f_name']
        l_name = data['_Employer__l_name']
        mail = data['_Employer__mail']
        psw = data['_Employer__psw']
        company = data['_Employer__company']

        return Employer(emp_id, f_name, l_name, mail, psw, company)


class Offer(Item):
    """
    Offer POPO
    """

    @not_none('id', 'title', 'state', 'description', 'location_type')
    def __init__(self,
                 id: int,
                 title: str,
                 state: str,
                 description: str,
                 employer: Employer = None,
                 location_type: str = '',
                 location: str | None = None,
                 required_skills: list[Skill] | None = None,
                 required_languages: list[Language] | None = None):
        self.__id: int = id
        self.__title: str = title
        self.__state: str = state
        self.__description: str = description
        self.__employer = employer
        self.__location_type: str = location_type
        self.__location = location
        self.__skills = required_skills
        self.__languages = required_languages

    @staticmethod
    def from_dict(data: dict) -> Offer:
        offer_id = data['_Offer__id']
        title = data['_Offer__title']
        desc = data['_Offer__description']
        state = data['_Offer__state']
        loc_type = data['_Offer__location_type']
        skill_data = data['_Offer__skills']
        skills = Skill.from_list(skill_data)
        # location = data['_Offer__location']
        try:
            emp_data = data['_Offer__employer']
            language_data = data['_Offer__languages']
            employer = Employer.from_dict(emp_data)
            languages = []
            for lang in language_data:
                languages.append(Language.from_dict(lang))
        except Exception:
            return Offer(
                id=offer_id,
                title=title,
                state=state,
                description=desc,
                location_type=loc_type,
                required_skills=skills,
            )

        return Offer(
            id=offer_id,
            title=title,
            state=state,
            description=desc,
            employer=employer,
            location_type=loc_type,
            required_skills=skills,
            required_languages=languages
        )

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
    def employer(self):
        return self.__employer

    @property
    def skills(self):
        return self.__skills

    @skills.setter
    def skills(self, value: list[Skill]):
        if value:
            self.__skills = value

    def __str__(self):
        return (f'[{self.__id}]: {self.__title} ({self.__state})\n'
                f'Employer: \n{self.__employer}\n'
                f'Location: {self.__location_type}, {(self.__location or None)}\n'
                f'RequiredSkills: \n{self.__skills}\n'
                f'Languages: \n{self.__languages}\n'
                f'Description:\n{self.__description}\n')
