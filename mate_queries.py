'''
Queries for all the relation types.
'''

# Third party imports
# - N/A

# Local imports
# - N/A


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
        '''.format(gid, sex),
        '': '''

        ''',
    }