# 3rd party imports
import sqlite3
import os

# Local imports
# - N/A

DATABASE_PATH = 'gorilla.db'


def get_or_create_connection(db_path=DATABASE_PATH, destroy_if_exists=False):
    if destroy_if_exists is True:
        if os.path.exists(db_path):
            os.remove(db_path)
    return sqlite3.connect(db_path)


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
        print("Create table Error: ", ex)


def insert_or_update_gorilla(gorilla, connection):
    try:
        record_exist = False
        cursor = connection.cursor()
        cursor.execute(
            "SELECT COUNT(*) from gorilla where gid='{}'".format(gorilla.identifier))
        (number_of_rows,) = cursor.fetchone()
        record_exist = number_of_rows > 0
        script = ''
        print('Record exists: ', record_exist)
        if record_exist:
            is_alive = None
            if gorilla.alive:
                is_alive = 1 if gorilla.alive is True else 0
            script = '''
                UPDATE gorilla SET
                    alive=IFNULL(alive, '{}'),
                    sex=IFNULL(sex, '{}'),
                    sire=IFNULL(sire, '{}'),
                    dam=IFNULL(dam, '{}')

                WHERE gid='{}'
            '''.format(
                is_alive or 'null',
                gorilla.sex or 'null',
                gorilla.sire or 'null',
                gorilla.dam or 'null',
                gorilla.identifier
            )
        else:
            script = '''
                INSERT INTO gorilla(gid, name, link, alive, sex, sire, dam)
                VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}')
            '''.format(
                gorilla.identifier, gorilla.name,
                gorilla.link, gorilla.alive or 'null',
                gorilla.sex or 'null', gorilla.sire or 'null',
                gorilla.dam or 'null'
            )
        script = script.replace("'null'", 'null')
        cursor.execute(script)
        connection.commit()
        print("Gorilla {} inserted/updated successfully.".format(
            gorilla.identifier))
    except Exception as ex:
        print("Insert/Update Gorilla Error: ", ex)
    finally:
        pass
        # connection.close()


def insert_sibling(gorilla, sibling, connection):
    try:
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO siblings(gid, sibling_id) VALUES('{}', '{}')
        '''.format(gorilla.identifier, sibling.identifier))
        connection.commit()
        print("Sibling {} of gorilla {} inserted successfully.".format(
            sibling.identifier, gorilla.identifier))
    except Exception as ex:
        print("Insert Sibling Error: ", ex)
    finally:
        pass
        # connection.close()


def insert_offspring(gorilla, offspring, connection):
    try:
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO offsprings(gid, offspring_id) VALUES('{}', '{}')
        '''.format(gorilla.identifier, offspring.identifier))
        connection.commit()
        print("Offspring {} of gorilla {} inserted successfully.".format(
            offspring.identifier, gorilla.identifier))
    except Exception as ex:
        print("Insert offspring Error: ", ex)
    finally:
        pass
        # connection.close()
