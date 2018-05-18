'''
Queries for all the relation types.
'''

# Third party imports
import string

# Local imports
# - N/A


def get_alphabet(number):
    d = dict(enumerate(string.ascii_lowercase, 1))
    return d[number]


def build_grandparent_query(level, offspring_id):
    return_string = '''
        SELECT gid FROM offsprings off WHERE off.offspring_id='{0}'
    '''.format(offspring_id)
    for i in range(level):
        return_string = '''
            SELECT gid FROM offsprings {0} WHERE {0}.offspring_id IN
            (
                {1}
            )
        '''.format(get_alphabet(i + 1), return_string)
    return return_string


def build_cousin_query(level, grandparents_query):
    return_string = '''
        SELECT offspring_id FROM offsprings grand WHERE grand.gid IN ({0})
    '''.format(grandparents_query)
    for i in range(level):
        return_string = '''
            SELECT offspring_id FROM offsprings {0} WHERE {0}.gid IN
            (
                {1}
            )
        '''.format(get_alphabet(i + 1), return_string)
    return return_string


def build_removed_cousin_query(offspring_id, level=1):
    # get the two fathers at different levels
    left_parent_query = build_grandparent_query(level, offspring_id)
    right_parent_query = build_grandparent_query(level + 1, offspring_id)
    return '''
        SELECT offspring_id FROM offsprings grand WHERE grand.gid IN ({0})
        AND grand.gid IN ({1})
    '''.format(left_parent_query, right_parent_query)
    # Build grandfathers query,
    # Build greatgrandfathers query,
    # Get offsprings that are from a combination of both.
    pass


def build_query(gid, sex):
    parent_label = 'sire' if sex == 'M' else 'dam'
    return {
        'grand_children': '''
                SELECT offspring_id FROM offsprings a
                LEFT JOIN gorilla b ON a.offspring_id = b.gid
                WHERE a.gid IN (
                    SELECT offspring_id FROM offsprings c
                    LEFT JOIN gorilla d ON c.offspring_id = d.gid
                    WHERE c.gid='{0}' AND d.sex='{1}'
                ) AND b.sex='{1}'
            '''.format(gid, sex),
        'grand_parents': '''
                SELECT {0} FROM gorilla a WHERE a.gid=(
                    SELECT {0} FROM gorilla b WHERE b.gid='{1}'
                )
        '''.format(parent_label, gid),
        'aunts_uncles': '''
            SELECT sibling_id FROM siblings a
            LEFT JOIN gorilla c ON (a.sibling_id = c.gid OR a.gid = c.gid)
            WHERE (
                a.gid=(
                    SELECT sire FROM gorilla WHERE gid='{0}'
                ) OR a.gid=(
                    SELECT dam FROM gorilla WHERE gid='{0}'
                )
            ) AND (c.sex='{1}')
        '''.format(gid, sex),
        'nephews': '''
            SELECT offspring_id FROM offsprings b
            LEFT JOIN gorilla c ON b.offspring_id = c.gid
            WHERE b.gid IN (
                 SELECT sibling_id FROM siblings a WHERE a.gid='{0}'
            ) AND c.sex='{1}'
        '''.format(gid, sex),
        'half_siblings': '''
            SELECT sibling_id FROM siblings a
            LEFT JOIN gorilla c ON a.sibling_id = c.gid
            WHERE a.gid='{0}' AND (
                c.sire <> (
                    SELECT sire FROM gorilla WHERE gid='{0}'
                ) OR c.dam <> (
                    SELECT dam FROM gorilla WHERE gid='{0}'
                )
            ) AND c.sex='{1}'
        '''.format(gid, sex)
    }
