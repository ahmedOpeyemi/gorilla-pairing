# Gorilla Pairing

This app attempts to pair gorillas for mating based on the genetic diversity between them. It uses http://www.dewarwildlife.org/ as the source of its gorillas and thier relationships.

## How it works
It scrapes the studbook available at the url above and pulls the following data for each gorilla:

- Name
- Sex
- Alive or dead
- Father (Sire)
- Mother (Dam)
- Siblings
- Offsprings

This data helps build a family tree for a specific gorilla and it is stored in a SQLite database.
Using the family tree built, for a specific gorilla, it determines the siblings, children, parents, grand children, grand parents, aunts, uncles, nephews, half siblings and cousins and assign percentage values that represents thier genetic relation. Gorillas that don't fall into these listed groups, have a genetic relation of 0%.

### How to run it
#### Prerequisites
 - Python 3.x
 - Pip

#### Install the dependencies
```
pip install -r requirements.txt
```

#### To build the data store.
```
python fetch.py
```
This step is optional if you have a gorilla.db file.

#### To determine suitable mates for a gorilla
```
python pair.py <identifier or resource name of the gorilla>

# Example:

python pair.py 1867.htm-BAKARI
```
This output a dictionary that has all the possible mates as keys, and % relation as values.

### Contributing
// TODO.