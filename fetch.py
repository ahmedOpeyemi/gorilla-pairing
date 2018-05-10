'''
Crawl the studbook for all the gorillas in the US region.
'''

# Third party imports
from bs4 import BeautifulSoup
import re

# Local imports
from remote import getPage
from db import (
    create_tables,
    get_or_create_connection,
    insert_or_update_gorilla,
    insert_offspring,
    insert_sibling
)
from gorilla import Gorilla

HTML_PARSER = 'html.parser'
ALL_ZOOS = []

SEX_LABEL = "Sex"
DATE_OF_DEATH_LABEL = "Date of death"
FATHER_LABEL = "Sire"
MOTHER_LABEL = "Dam"

HREF_TAG = 'href'

DB_CONNECTION = None


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
    name = str(name).replace("'", "").replace(
        "*", "").replace("½", "").strip().replace(" ", "_")
    href = str(href).strip()
    return '{}-{}'.format(href, name)


def get_name_link(identifier):
    halves = identifier.replace("_", " ").split('-')
    return halves[0], halves[1]


def get_gorilla_info(gorilla_route, with_siblings_and_offsprings=True):
    gorilla = Gorilla(alive=True, link=gorilla_route)
    gorilla_page_dom = BeautifulSoup(getPage(gorilla_route), HTML_PARSER)
    name = (gorilla_page_dom.find_all("font", attrs={"size": 5})[0]).string
    gorilla.name = name
    gorilla.identifier = make_identifier(gorilla_route, name)
    sex_tag = gorilla_page_dom.find_all(string=re.compile(SEX_LABEL))[0]
    if sex_tag:
        gorilla.sex = "F" if "Female" in sex_tag.string else "M"
    date_of_death_tag = gorilla_page_dom.find_all(
        string=re.compile(DATE_OF_DEATH_LABEL)
    )
    if len(date_of_death_tag) > 0:
        gorilla.alive = False

    def get_parent_identifier(parent_label):
        parent_tag = gorilla_page_dom.find(
            string=re.compile(parent_label)
        ).parent.find("a")
        if parent_tag:
            parent_name = parent_tag.string
            parent_href = parent_tag.get(HREF_TAG)
            return make_identifier(parent_href, parent_name)
        return None

    gorilla.sire = get_parent_identifier(FATHER_LABEL)
    gorilla.dam = get_parent_identifier(MOTHER_LABEL)

    if with_siblings_and_offsprings:
        print('Getting gorilla siblings')
        siblings_header_tag = gorilla_page_dom.find(
            text=re.compile("Siblings")).parent.parent
        siblings_tag = siblings_header_tag.find_next_sibling("p")
        has_completed_siblings_tag = False
        if siblings_tag:
            for sibling in siblings_tag.find_next_siblings():
                if sibling.name == 'a' and has_completed_siblings_tag is False:
                    gorilla.siblings.append(
                        make_identifier(sibling.get(HREF_TAG), sibling.string))
                elif sibling.name == 'font':
                    if len(sibling.find_all(text=re.compile("Offspring"))) > 0:
                        has_completed_siblings_tag = True
                elif sibling.name == 'a' and has_completed_siblings_tag is True:
                    gorilla.offsprings.append(
                        make_identifier(sibling.get(HREF_TAG), sibling.string))
    return gorilla


def save_gorilla(gorilla):
    insert_or_update_gorilla(gorilla, DB_CONNECTION)
    print("Gorilla object built, attempting to save: ", gorilla.identifier, gorilla.link, gorilla.alive)
    for sibling_identifier in gorilla.siblings:
        (href, name) = get_name_link(sibling_identifier)
        sibling_gorilla = get_gorilla_info(
            href,
            with_siblings_and_offsprings=False
        )
        insert_or_update_gorilla(sibling_gorilla, DB_CONNECTION)
        insert_sibling(gorilla, sibling_gorilla, DB_CONNECTION)
        print("Gorilla siblings saved: ", sibling_gorilla.identifier, gorilla.identifier)
    # TODO: Duplicate code here, fix.
    for offspring_identifier in gorilla.offsprings:
        (href, name) = get_name_link(offspring_identifier)
        offspring_gorilla = get_gorilla_info(
                        href,
                        with_siblings_and_offsprings=False
                    )
        insert_or_update_gorilla(offspring_gorilla, DB_CONNECTION)
        insert_offspring(gorilla, offspring_gorilla, DB_CONNECTION)
        print("Gorilla offspring saved: ", offspring_gorilla.identifier, gorilla.identifier)


if __name__ == '__main__':
    DB_CONNECTION = get_or_create_connection()
    create_tables(DB_CONNECTION)
    get_all_links("USAmenu.htm", add_zoo)
    zoo_index = 0
    if len(ALL_ZOOS) > 0:
        for zoo_route in ALL_ZOOS:
            zoo_index = zoo_index + 1
            print('''

            Collecting gorilla data from zoo {}: {}

            '''.format(zoo_index, zoo_route))
            page_dom = BeautifulSoup(getPage(zoo_route), HTML_PARSER)
            for link in page_dom.find_all('a'):
                href = link.get(HREF_TAG)
                gorilla = get_gorilla_info(
                    href,
                    with_siblings_and_offsprings=True
                )
                save_gorilla(gorilla)

