'''
Queries for all the relation types.
'''

# Third party imports
# - N/A

# Local imports
# - N/A


def build_query(gid, sex):
    return {
        'grand_children': '''
                SELECT offspring_id FROM offsprings WHERE gid IN (
                    SELECT offspring_id FROM offsprings WHERE gid='{0}'
                    AND sex='{1}'
                ) AND sex='{1}'
            '''.format(gid, sex)
    }
