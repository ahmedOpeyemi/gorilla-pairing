# Third party imports
from bs4 import BeautifulSoup
import re

# Local imports
from remote import getPage

HTML_PARSER = 'html.parser'
ALL_ZOOS = []

SEX_LABEL = "Sex"
DATE_OF_DEATH_LABEL = "Date of death"
FATHER_LABEL = "Sire"
MOTHER_LABEL = "Dam"

HREF_TAG = 'href'


def get_all_links(page_route, each_link_callback=None):
    page_dom = BeautifulSoup(getPage(page_route), HTML_PARSER)
    for link in page_dom.find_all('a'):
        href = link.get(HREF_TAG)
        if each_link_callback:
            each_link_callback(href)


def add_zoo(zoo_route):
    # print("Zoo: ", zoo_route)
    ALL_ZOOS.append(zoo_route)


def make_identifier(href, name):
    name = str(name).strip()
    href = str(href).strip()
    return '{}-{}'.format(href, name)


def get_gorilla_info(gorilla_route):
    gorilla = {
        'link': gorilla_route,
        'alive': True,
        'sex': None,
        'siblings': [],
        'offspring': [],
        'sire': None,  # Father
        'dam': None,  # Mother
    }
    gorilla_page_dom = BeautifulSoup(getPage(gorilla_route), HTML_PARSER)
    sex_tag = gorilla_page_dom.find_all(string=re.compile(SEX_LABEL))[0]
    if sex_tag:
        gorilla['sex'] = "Female" if "Female" in sex_tag.string else "Male"
    date_of_death_tag = gorilla_page_dom.find_all(
        string=re.compile(DATE_OF_DEATH_LABEL)
    )
    if len(date_of_death_tag) > 0:
        gorilla['alive'] = False
    siblings_header_tag = gorilla_page_dom.find(text=re.compile("Siblings")).parent.parent
    siblings_tag = siblings_header_tag.find_next_sibling("p")
    has_completed_siblings_tag = False
    if siblings_tag:
        for sibling in siblings_tag.find_next_siblings():
            if sibling.name == 'a' and has_completed_siblings_tag == False:
                gorilla['offspring'].append(make_identifier(sibling.get(HREF_TAG), sibling.string))
            elif sibling.name == 'font':
                print('font value >>> ', sibling.string)
            '''
            for each sibling, check if it is a, if yes, get the name, if not,
            check if it is offspring text, if yes, then offspring listing has started, if yes,
            all others shold be marked as offsprings
            '''
        # print('siblings tag >>>', siblings_tag.children, siblings_tag.descendants, siblings_tag.contents)

    print('Gorilla >>>', gorilla)


get_all_links("USAmenu.htm", add_zoo)
if len(ALL_ZOOS) > 0:
    for zoo_route in ALL_ZOOS:
        get_all_links(zoo_route, get_gorilla_info)
        break
