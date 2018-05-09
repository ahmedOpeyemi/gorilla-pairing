# 3rd party imports
import sqlite3
import os

# Local imports
# - N/A

DATABASE_PATH = 'gorilla.db'


def get_or_create_connection(db_path, destroy_if_exists=False):
    if destroy_if_exists is True:
        if os.path.exists(DATABASE_PATH):
            os.remove(DATABASE_PATH)
    return sqlite3.connect(DATABASE_PATH)


def create_tables(connection):
    CREATE_GORILLA_TABLE_SCRIPT = '''
        CREATE TABLE IF NOT EXISTS gorilla(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gid TEXT UNIQUE,
            name TEXT,
            link TEXT UNIQUE,
            alive INTEGER NULL,
            sex TEXT NULL,
            sire TEXT NULL,
            dam TEXT NULL,
            FOREIGN KEY(sire) REFERENCES gorilla(gid)
            FOREIGN KEY(dam) REFERENCES gorilla(gid)
        )
    '''

    CREATE_SIBLINGS_TABLE_SCRIPT = '''
        CREATE TABLE IF NOT EXISTS siblings(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gid TEXT,
            sibling_id TEXT,
            FOREIGN KEY(gid) REFERENCES gorilla(gid)
            FOREIGN KEY(sibling_id) REFERENCES gorilla(gid)
        )
    '''

    CREATE_OFFSPRINGS_TABLE_SCRIPT = '''
        CREATE TABLE IF NOT EXISTS offsprings(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gid TEXT,
            offspring_id TEXT,
            FOREIGN KEY(gid) REFERENCES gorilla(gid)
            FOREIGN KEY(offspring_id) REFERENCES gorilla(gid)
        )
    '''

    cur = connection.cursor()
    for table_script in [
        CREATE_GORILLA_TABLE_SCRIPT,
        CREATE_SIBLINGS_TABLE_SCRIPT,
        CREATE_OFFSPRINGS_TABLE_SCRIPT
    ]:
        cur.execute(table_script)


def insert_or_update_gorilla(gorilla):
    pass


def insert_sibling(gorilla, sibling):
    pass


def insert_offspring(gorilla, offspring):
    pass
