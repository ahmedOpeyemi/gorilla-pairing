# Third party imports
from bs4 import BeautifulSoup

# Local imports
from remote import getPage

HTML_PARSER = 'html.parser'
ALL_ZOOS = []
ALL_GORILLAS = []


def get_all_links(page_route, each_link_callback=None):
    page_dom = BeautifulSoup(getPage(page_route), HTML_PARSER)
    for link in page_dom.find_all('a'):
        href = link.get('href')
        if each_link_callback:
            each_link_callback(href)


def add_zoo(zoo_route):
    print("Zoo: ", zoo_route)
    ALL_ZOOS.append(zoo_route)


def get_gorilla_info(gorilla_route):
    print("Gorilla: ", gorilla_route)


get_all_links("USAmenu.htm", add_zoo)
if len(ALL_ZOOS) > 0:
    for zoo_route in ALL_ZOOS:
        get_all_links(zoo_route, get_gorilla_info)
