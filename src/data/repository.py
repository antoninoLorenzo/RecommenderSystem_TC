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

    def get_all_developers(self) -> list[Developer]:
        """
        Make a query to the database using pandas
        """
        result: DataFrame = read_sql_query(
            f'''
            SELECT d.developerId, d.firstName, d.lastName, d.bio, d.mail, d.passwordAccount, d.locationId
            from developer d
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

    def get_location(self, location_id=None, developer_id=None) -> Location:
        '''
        Retrieves one location based off of its ID or the ID of the developer who references it
        location_id will be used if both are not None
        '''
        if location_id is None and developer_id is None:
            raise AttributeError('No attributes input')

        if location_id is not None:
            df = read_sql_query(
                f'''
                SELECT *
                FROM location l
                WHERE l.locationId = {location_id}
                ''',
                self.__session.connection()
            )
        else:
            df = read_sql_query(
                f'''
                SELECT l.locationId, l.loc_name, l.lat, l.lon
                FROM location l, developer d 
                WHERE d.developerId = {developer_id} AND d.locationId = l.locationId
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

if __name__ == '__main__':
    dr = DeveloperRepository()

    for s in dr.get_developer(1).skills:
        print(s.name)
