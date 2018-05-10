'''
Gorilla class
'''

# Third party imports
# - N/A

# Local imports
# - N/A


class Gorilla:
    def __init__(self, identifier=None, name=None, link=None, alive=None,
                 sex=None, siblings=[], offsprings=[], sire=None, dam=None):
        self.identifier = identifier
        self.name = name
        self.link = link
        self.alive = alive
        self.sex = sex
        self.siblings = siblings
        self.offsprings = offsprings
        self.sire = sire
        self.dam = dam

    def __str__(self):
        return '''
            Name: {}, Sex: {}, Link: {}
        '''.format(self.name, self.sex, self.link)
