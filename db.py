'''
Handles all CRUD operations
'''

# 3rd party imports
import sqlite3
import os
import traceback

# Local imports
from gorilla import Gorilla

DATABASE_PATH = 'gorilla.db'
# TABLES = {
#     'GORILLA': 'gorilla',
#     'OFFSPRINGS': 'offsprings',
#     'SIBLINGS': 'siblings'
# }


def get_or_create_connection(db_path=DATABASE_PATH,
                             fail_if_db_doesnt_exist=False):
    if fail_if_db_doesnt_exist is True:
        if not os.path.exists(db_path):
            raise Exception('''
                Database does not exist, do you want to run fetch.py first?
                ''')
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
                FOREIGN KEY(sibling_id) REFERENCES gorilla(gid),
                UNIQUE(gid, sibling_id)
            )
        '''

        CREATE_OFFSPRINGS_TABLE_SCRIPT = '''
            CREATE TABLE IF NOT EXISTS offsprings(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                gid TEXT,
                offspring_id TEXT,
                FOREIGN KEY(gid) REFERENCES gorilla(gid)
                FOREIGN KEY(offspring_id) REFERENCES gorilla(gid),
                UNIQUE(gid, offspring_id)
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
    # TODO: clean up some redundant checks here.
    try:
        record_exist = False
        cursor = connection.cursor()
        cursor.execute(
            "SELECT COUNT(*) from gorilla where gid='{}'".format(
                gorilla.identifier))
        (number_of_rows,) = cursor.fetchone()
        record_exist = number_of_rows > 0
        script = ''
        # print('Record exists: ', record_exist)
        is_alive = None
        if gorilla.alive is True:
            is_alive = 1
        elif gorilla.alive is False:
            is_alive = 0

        if record_exist:
            script = '''
                UPDATE gorilla SET
                    alive=IFNULL(alive, '{}'),
                    sex=IFNULL(sex, '{}'),
                    sire=IFNULL(sire, '{}'),
                    dam=IFNULL(dam, '{}')

                WHERE gid='{}'
            '''.format(
                'null' if is_alive is None else is_alive,
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
                gorilla.identifier, gorilla.name.replace("'", ""),
                gorilla.link or 'null', (
                    'null' if is_alive is None else is_alive),
                gorilla.sex or 'null', gorilla.sire or 'null',
                gorilla.dam or 'null'
            )
        script = script.replace("'null'", 'null')
        cursor.execute(script)
        connection.commit()
        # print("Gorilla {} inserted/updated successfully.".format(
        #     gorilla.identifier))
    except Exception as ex:
        print("Insert/Update Gorilla Error: ", ex, gorilla.identifier)
    finally:
        pass
        # connection.close()


def insert_sibling(gorilla, sibling, connection):
    try:
        cursor = connection.cursor()
        cursor.execute(
            '''
            SELECT COUNT(*) from siblings where gid="{}" and sibling_id="{}"
            '''.format(gorilla.identifier, sibling.identifier))
        (number_of_rows,) = cursor.fetchone()
        record_exist = number_of_rows > 0
        if not record_exist:
            cursor.execute('''
                INSERT INTO siblings(gid, sibling_id) VALUES('{}', '{}')
            '''.format(gorilla.identifier, sibling.identifier))
            connection.commit()
            # print("Sibling {} of gorilla {} inserted successfully.".format(
            #     sibling.identifier, gorilla.identifier))
    except Exception as ex:
        print("Insert Sibling Error: ", ex,
              gorilla.identifier, sibling.identifier)
    finally:
        pass
        # connection.close()


def insert_offspring(gorilla, offspring, connection):
    try:
        cursor = connection.cursor()
        cursor.execute(
            '''
            SELECT COUNT(*) from offsprings where
            gid="{}" and offspring_id="{}"
            '''.format(gorilla.identifier, offspring.identifier))
        (number_of_rows,) = cursor.fetchone()
        record_exist = number_of_rows > 0
        if not record_exist:
            cursor.execute(
                '''
                INSERT INTO offsprings(gid, offspring_id) VALUES('{}', '{}')
                '''.format(gorilla.identifier, offspring.identifier))
            connection.commit()
            # print("Offspring {} of gorilla {} inserted successfully.".format(
            #     offspring.identifier, gorilla.identifier))
    except Exception as ex:
        print("Insert offspring Error: ", ex,
              gorilla.identifier, offspring.identifier)
    finally:
        pass
        # connection.close()


def get_gorilla(identifier_or_link, with_parents=False,
                with_siblings_and_offsprings=False,
                fail_if_dead=True,
                connection=None):
    if not connection:
        connection = get_or_create_connection(fail_if_db_doesnt_exist=True)
    gorilla = None
    try:
        cursor = connection.cursor()
        script = '''
            SELECT * FROM gorilla WHERE gid='{0}' OR link='{0}' LIMIT 1
        '''.format(identifier_or_link)
        cursor.execute(script)

        for row in cursor:
            gorilla = Gorilla(
                identifier=row[1],
                name=row[2],
                link=row[3],
                alive=row[4] == 1,
                sex=row[5],
                sire=get_gorilla(row[6]) if with_parents is True else row[6],
                dam=get_gorilla(row[7]) if with_parents is True else row[7]
            )
        if gorilla is not None:
            if fail_if_dead and gorilla.alive is False:
                return gorilla
            if with_siblings_and_offsprings:
                script = '''
                    SELECT sibling_id FROM siblings WHERE gid='{}'
                '''.format(gorilla.identifier)
                cursor.execute(script)
                siblings = []
                for row in cursor:
                    siblings.append(
                        get_gorilla(row[0])
                    )
                script = '''
                    SELECT offspring_id FROM offsprings WHERE gid='{}'
                '''.format(gorilla.identifier)
                cursor.execute(script)
                offsprings = []
                for row in cursor:
                    offsprings.append(
                        get_gorilla(row[0])
                    )
                gorilla.siblings = siblings
                gorilla.offsprings = offsprings
    except Exception as ex:
        print("Error trying to get gorilla record: ", ex)
        traceback.print_exc()
    finally:
        connection.close()
    return gorilla
