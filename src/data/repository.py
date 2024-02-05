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
from src.data.entity import Developer


class DeveloperRepository:
    """
    Used to interact with Developer table in Turing Careers database
    """

    def __init__(self):
        self.__session: Session = DatabaseEngineFactory.get_instance()

    def search_developers(self, query: str) -> list[Developer]:
        """
        Make a query to the database using pandas
        """
        result: DataFrame = read_sql_query(
        f'''
            SELECT * FROM Developer WHERE MATCH(bio) 
            AGAINST({query} IN NATURAL LANGUAGE MODE);''',
            self.__session.connection()
        )

        print(result)

        return []
