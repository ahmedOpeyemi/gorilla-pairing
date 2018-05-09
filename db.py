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
    try:
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

        cursor = connection.cursor()
        for table_script in [
            CREATE_GORILLA_TABLE_SCRIPT,
            CREATE_SIBLINGS_TABLE_SCRIPT,
            CREATE_OFFSPRINGS_TABLE_SCRIPT
        ]:
            cursor.execute(table_script)
            connection.commit()
    except Exception as ex:
        print("Error: ", ex)


# TODO: A lot of field repetition in this project. Use constants to replace.


def insert_or_update_gorilla(gorilla, connection):
    try:
        record_exist = False
        cursor = connection.cursor()
        cursor.execute(
            "SELECT COUNT(*) from gorilla where gid={}".format(gorilla['gid']))
        (number_of_rows,) = cursor.fetchone()
        record_exist = number_of_rows > 0
        script = ''
        if record_exist:
            script = '''
                UPDATE gorilla SET (
                    alive=coalesce(alive, {}),
                    sex=coalesce(sex, {}),
                    sire=coalesce(sire, {}),
                    dam=coalesce(dam, {})
                )
                WHERE gid={}
            '''.format(
                1 if gorilla['alive'] is True else 0,
                gorilla['sex'],
                gorilla['sire'],
                gorilla['dam'],
                gorilla['gid']
            )
        else:
            script = '''
                INSERT INTO gorilla(gid, name, link, alive, sex, sire, dam)
                VALUES({}, {}, {}, {}, {}, {}, {})
            '''.format(
                gorilla['gid'], gorilla['name'],
                gorilla['link'], gorilla['alive'],
                gorilla['sex'], gorilla['sire'],
                gorilla['dam']
            )
        cursor.execute(script)
        connection.commit()
        print("Gorilla {} inserted/updated successfully.".format(
            gorilla['gid']))
    except Exception as ex:
        print("Error: ", ex)
    finally:
        pass
        # connection.close()



def insert_sibling(gorilla, sibling):
    pass


def insert_offspring(gorilla, offspring):
    pass
