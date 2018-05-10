'''
Pairs one or more gorillas with suitable mate(s)
'''

# Third party imports
import sys

# Local imports
from db import (
    get_gorilla
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
    pass


if __name__ == '__main__':
    args = sys.argv[:1]
    if 'all' in args:
        # Run for all gorillas
        pass
    else:
        gorilla = get_gorilla(
            args[0],
            with_parents=True,
            with_siblings_and_offsprings=True
        )
        mates = find_best_mates(gorilla)
        print('Mate(s) >>', mates)
