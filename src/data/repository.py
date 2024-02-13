"""
Contains classes to interact with database.
"""
import sys

# --- Try import sqlalchemy
try:
    from pandas import DataFrame, read_sql_query
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session, sessionmaker
    from sqlalchemy.exc import SQLAlchemyError
except ImportError as import_err:
    print(f'[!] {import_err}')
    sys.exit(1)

from src.data import DatabaseEngineFactory
from src.data.entity import *


def get_offers_frame(offer_list: list[Offer]):
    offers_dict = []
    for o in offer_list:
        skill_set = {s.name for s in o.skills}
        offers_dict.append({
            'id': o.id,
            'Title': o.title,
            'RequiredSkills': skill_set
        })
    return DataFrame(offers_dict)


def get_developers_frame(developer_list: list[Developer]):
    developers_dict = []
    for d in developer_list:
        skills_set = {s.name for s in d.skills}
        developers_dict.append({
            'id': d.developer_id,
            'Skills': skills_set
        })
    return DataFrame(developers_dict)


class SkillRepository:
    def __init__(self):
        self.__session: Session = DatabaseEngineFactory.get_instance().session

    @not_none('developer_id')
    def get_developer_skills(self, developer_id: int) -> list[Skill]:
        '''
        Retrieves the list of skills of a developer
        '''
        df: DataFrame = read_sql_query(
            f'''
            SELECT s.skillId, s.skill_name, s.skill_type
            FROM DeveloperSkill jt, Skill s 
            WHERE jt.developerId = {developer_id} AND jt.skillId = s.skillId
            ''',
            self.__session.connection()
        )

        skills = []
        for _, row in df.iterrows():
            skill = Skill(
                row.skillId,
                row.skill_name,
                row.skill_type
            )

            skills.append(skill)

        return skills

    @not_none('offer_id')
    def get_offer_skills(self, offer_id: int) -> list[Skill]:
        '''
        Retrievs the list of skills of an offer
        '''
        df: DataFrame = read_sql_query(
            f'''
            SELECT s.skillId, s.skill_name, s.skill_type
            FROM OfferSkill jt, skill s 
            WHERE jt.offerId = {offer_id} AND jt.skillId = s.skillId
            ''',
            self.__session.connection()
        )

        skills = []
        for _, row in df.iterrows():
            skill = Skill(
                row.skillId,
                row.skill_name,
                row.skill_type
            )

            skills.append(skill)

        return skills


class DeveloperRepository:
    """
    Used to interact with Developer table in Turing Careers database
    """

    def __init__(self):
        self.__session: Session = DatabaseEngineFactory.get_instance().session

    def get_developers(self, query=None) -> list[Developer]:
        """
        Make a query to the database using pandas
        """
        if query is None:
            result: DataFrame = read_sql_query(
                '''
                SELECT *
                FROM developer d
                JOIN developerlanguage dl ON d.developerId = dl.developerId
                JOIN Language l ON dl.languageId = l.languageId
                ''',
                self.__session.connection()
            )
        else:
            result: DataFrame = read_sql_query(
                f'''
                SELECT *
                FROM developer d 
                WHERE MATCH(d.bio)
                AGAINST('{query}' IN NATURAL LANGUAGE MODE)
                ''',
                self.__session.connection()
            )

        devs = []
        # loc_repo = LocationRepository()
        skill_repo = SkillRepository()
        for _, row in result.iterrows():
            dev_lang = Language(row.languageId, row.languageCode)
            # dev_loc = loc_repo.get_location(location_id=row.locationId)
            dev_skills = skill_repo.get_developer_skills(row.developerId.iloc[0])

            dev = Developer(
                dev_id=row.developerId,
                f_name=row.firstName,
                l_name=row.lastName,
                bio=row.bio,
                mail=row.mail,
                psw=row.passwordAccount,
                languages=[dev_lang],
                location=row.locationName,  # location=dev_loc,
                skills=dev_skills
            )

            devs.append(dev)

        return devs

    @not_none('developer_id')
    def get_developer(self, developer_id) -> Developer:
        '''
        Retrieves one developer based off of its id
        '''
        df: DataFrame = read_sql_query(
            f'''
                    SELECT d.developerId, d.firstName, d.lastName, d.bio, d.mail, d.passwordAccount, d.locationName
                    from developer d
                    WHERE d.developerId = {developer_id}
                    ''',
            self.__session.connection()
        )

        # locRepo = LocationRepository()
        skill_repo = SkillRepository()
        for i, row in df.iterrows():
            if i != 0:
                raise Exception(f'fetch of single item returned multiple ({len(df)})')
            dev = Developer(
                row.developerId,
                row.firstName,
                row.lastName,
                row.bio,
                row.mail,
                row.passwordAccount,
                row.locationName,  # locRepo.get_location(location_id=row.locationId),
                skill_repo.get_developer_skills(row.developerId)
            )

        return dev


"""
class LocationRepository:
    def __init__(self):
        self.__session: Session = DatabaseEngineFactory.get_instance().session

    def get_location(self, location_id=None, developer_id=None, offer_id=None) -> Location:
        '''
        Retrieves one location based off of its ID or the ID of the developer who references it
        location_id will be used if multiple are not none
        developer_id will be used if it and offer_id are not none
        '''
        if location_id is None and developer_id is None and offer_id is None:
            raise AttributeError('All attributes are None, but at least one is needed')

        if location_id is not None:
            df = read_sql_query(
                f'''
                SELECT *
                FROM location l
                WHERE l.locationId = {location_id}
                ''',
                self.__session.connection()
            )
        elif developer_id is not None:
            df = read_sql_query(
                f'''
                SELECT l.locationId, l.loc_name, l.lat, l.lon
                FROM location l, developer d 
                WHERE d.developerId = {developer_id} AND d.locationId = l.locationId
                ''',
                self.__session.connection()
            )
        else:
            df = read_sql_query(
                f'''
                SELECT l.locationId, l.loc_name, l.lat, l.lon
                FROM location l, offer o 
                WHERE o.offerId = {offer_id} AND o.locationId = l.locationId
                ''',
                self.__session.connection()
            )

        for i, row in df.iterrows():
            if i != 0:
                raise Exception(f'fetch of single item returned multiple ({len(df)})')
            location = Location(
                row.locationId,
                row.loc_name,
                row.lat,
                row.lon
            )

        return location
"""


class OfferRepository:
    def __init__(self):
        self.__session: Session = DatabaseEngineFactory.get_instance().session

    def get_offers(self, query=None) -> list[Offer]:
        """
        Retrieves all offers and their locations
        """
        if query is None:
            df = read_sql_query(
                f'''
                SELECT *
                FROM offer
                ''',
                self.__session.connection()
            )
        else:
            df = read_sql_query(
                f'''
                SELECT *
                FROM offer o 
                WHERE MATCH(o.title, o.offerDescription)
                AGAINST('{query}' IN NATURAL LANGUAGE MODE)
                ''',
                self.__session.connection()
            )

        offers = []
        # locRepo = LocationRepository()
        skill_repo = SkillRepository()
        emp_repo = EmployerRepository()
        for _, row in df.iterrows():
            if row.locationType == 'Remote':
                _location = None
            else:
                _location = row.locationName # locRepo.get_location(offer_id=row.offerId)

            offer = Offer(
                id=row.offerId,
                title=row.title,
                state=row.state,
                description=row.offerDescription,
                employer=emp_repo.get_employer(row.employerId),
                required_skills=skill_repo.get_offer_skills(row.offerId),
                location_type=row.locationType,
                location=_location
            )

            offers.append(offer)

        return offers

    @not_none('offer_id')
    def get_offer(self, offer_id) -> Offer:
        '''
        Retrieves one offer based off of its ID
        '''

        df = read_sql_query(
            f'''
            SELECT *
            FROM offer o 
            WHERE o.offerId = {offer_id}
            ''',
            self.__session.connection()
        )

        # locRepo = LocationRepository()
        skill_repo = SkillRepository()
        emp_repo = EmployerRepository()
        for i, row in df.iterrows():
            if i != 0:
                raise Exception(f'fetch of single item returned multiple ({len(df)})')
            offer = Offer(
                id=row.offerId,
                title=row.title,
                state=row.state,
                description=row.offerDescription,
                employer=emp_repo.get_employer(row.employerId),
                required_skills=skill_repo.get_offer_skills(row.offerId),
                location_type=row.locationType,
                location=(None if row.locationType == 'Remote' else row.locationName)
                # locRepo.get_location(offer_id=row.offerId))
            )

        return offer


class EmployerRepository:
    def __init__(self):
        self.__session: Session = DatabaseEngineFactory.get_instance().session

    def get_employer(self, employer_id) -> Employer:
        '''
        Retrieves an employer based off of its id
        '''

        df = read_sql_query(
            f'''
            SELECT *
            FROM employer e 
            WHERE e.employerId = {employer_id}
            ''',
            self.__session.connection()
        )

        for i, row in df.iterrows():
            if i != 0:
                raise Exception(f'fetch of single item returned multiple ({len(df)})')

            employer = Employer(
                row.employerId,
                row.firstName,
                row.lastName,
                row.mail,
                row.passwordAccount,
                row.companyName
            )

        return employer


if __name__ == '__main__':
    dr = DeveloperRepository()

    for s in dr.get_developers('bio'):
        print(s.first_name)
