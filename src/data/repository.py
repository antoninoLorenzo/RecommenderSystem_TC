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
                f'''
                SELECT d.developerId, d.firstName, d.lastName, d.bio, d.mail, d.passwordAccount, d.locationId
                from developer d
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
        locRepo = LocationRepository()
        skillRepo = SkillRepository()
        for _, row in result.iterrows():
            dev = Developer(
                row.developerId,
                row.firstName,
                row.lastName,
                row.bio,
                row.mail,
                row.passwordAccount,
                locRepo.get_location(location_id=row.locationId),
                skillRepo.get_developer_skills(row.developerId)
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
                    SELECT d.developerId, d.firstName, d.lastName, d.bio, d.mail, d.passwordAccount, d.locationId
                    from developer d
                    WHERE d.developerId = {developer_id}
                    ''',
            self.__session.connection()
        )

        locRepo = LocationRepository()
        skillRepo = SkillRepository()
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
                locRepo.get_location(location_id=row.locationId),
                skillRepo.get_developer_skills(row.developerId)
            )

        return dev


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
                WHERE o.developerId = {offer_id} AND o.locationId = l.locationId
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


class OfferRepository:
    def __init__(self):
        self.__session: Session = DatabaseEngineFactory.get_instance().session

    def get_offers(self, query=None) -> list[Offer]:
        '''
        Retrieves all offers and their locations
        '''
        if query is None:
            df = read_sql_query(
                f'''
                SELECT *
                FROM offer
                '''
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
        locRepo = LocationRepository()
        skillRepo = SkillRepository()
        emplRepo = EmployerRepository()
        for _, row in df.iterrows():
            offer = Offer(
                row.offerId,
                row.title,
                row.state,
                row.offerDescription,
                emplRepo.get_employer(row.employerId),
                skillRepo.get_offer_skills(row.offerId),
                row.locationType,
                location=(None if row.locationType == 'Remote' else locRepo.get_location(offer_id=row.offerId))
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

        locRepo = LocationRepository()
        skillRepo = SkillRepository()
        emplRepo = EmployerRepository()
        for i, row in df.iterrows():
            if i != 0:
                raise Exception(f'fetch of single item returned multiple ({len(df)})')
            offer = Offer(
                row.offerId,
                row.title,
                row.state,
                row.offerDescription,
                emplRepo.get_employer(row.employerId),
                skillRepo.get_offer_skills(row.offerId),
                row.locationType,
                location=(None if row.locationType == 'Remote' else locRepo.get_location(offer_id=row.offerId))
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
            '''
        )

        for i, row in df.iterrows():
            if i != 0:
                raise Exception(f'fetch of single item returned multiple ({len(df)})')

            employer = Employer(
                row.employrId,
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