"""
Non Generation/Pattern Finding related methods
"""

import time
import sqlite3


def print_performance(fn):
    """
    Self explanation
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        out = fn(*args, **kwargs)
        end = time.time()
        print(f'Done in {end - start:.2f}')
        return out

    return wrapper


def create_table():
    """
    creates developer_dataset.db
    """
    conn = sqlite3.connect('developers_dataset.db')
    c = conn.cursor()
    c.execute("""
            CREATE TABLE IF NOT EXISTS developers (
             ID INTEGER PRIMARY KEY, 
             firstName TEXT,
             lastName TEXT,
             email TEXT,
             biography TEXT,
             professions,
             skills TEXT,
             languages TEXT,
             location TEXT
            )
            """
              )
    conn.commit()
    conn.close()


def insert_data(developer, table):
    """
    add items to developer_dataset.db
    """
    conn = sqlite3.connect('developers_dataset.db')
    c = conn.cursor()
    for i, out_dev in enumerate(developer):
        # --- TODO: fix the statement
        c.execute(f"INSERT INTO {table} VALUES ({i + 1}, '{out_dev}')")
    conn.commit()
    conn.close()
