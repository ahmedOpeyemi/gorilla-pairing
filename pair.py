'''
Pairs one or more gorillas with suitable mate(s)
'''

# Third party imports
import sys
import traceback

# Local imports
from db import (
    get_gorilla,
    get_relations
)


def find_best_mates(gorilla):
    '''
        1. Check if gorilla is alive, if no quit.
        2. Check sex, and for every of the sex:
            a. identify the:
                a. Twin
                b. Sibling
                c. Grandparent / Grandchild Aunt / Uncle Niece / Nephew / Half Sibling
                d. 1st Cousin
                e. 1st Cousin once removed
                f. 2nd Cousin
                g. 2nd Cousin once removed
                h. 3rd Cousin
                i. 4th Cousin
                j. 5th Cousin
                k. 6th Cousin
            b. for all the identified relatives, assign the percentages to them.
            c. for all the non relatives, add them to a list.
    '''
    mate_sex = 'F' if gorilla.sex == 'M' else 'M'
    relations = {
        'siblings': gorilla.siblings,
        'children': gorilla.offsprings,
        'parents': [gorilla.sire, gorilla.dam],
        'grand_children': [],
        'grand_parents': [],
        'aunts_uncles': [],
        'nephews': [],
        'half_siblings': [],
        'first_cousins': [],
        'second_cousins': [],
        'third_cousins': [],
        'fourth_cousins': [],
        'fifth_cousins': [],
        'sixth_cousins': [],
    }
    for key, value in relations.items():
        if value == []:
            relations[key] = get_relations(
                mate_sex, key, gorilla.identifier
            )
    return relations


GENERAL_ERROR = '''
            Error:
            Unrecognized argument supplied, please supply
            gorilla identifier or link or "all" to run the pairing
            for all gorillas in the database.
        '''


if __name__ == '__main__':
    try:
        args = sys.argv
        identifier_or_key = args[1]
        if len(args) < 1 or identifier_or_key == __file__:
            print(GENERAL_ERROR)
            quit()

        if 'all' in args:
            # Run for all gorillas
            pass
        elif identifier_or_key is not None:
            gorilla = get_gorilla(
                identifier_or_key,
                with_siblings_and_offsprings=True
            )
            if gorilla is not None:
                if gorilla.alive is False:
                    print('''
                        Gorilla {} is not alive.
                    '''.format(gorilla.identifier))
                    quit()
                print('''
                    Finding mates for {}
                '''.format(gorilla.identifier))
                mates = find_best_mates(gorilla)
                print('Mate(s) >>', mates)
        else:
            print(GENERAL_ERROR)
    except Exception as ex:
        print(ex)
        traceback.print_exc()
        print(GENERAL_ERROR)
