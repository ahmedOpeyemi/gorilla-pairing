# Third party imports
from bs4 import BeautifulSoup

# Local imports
from remote import getPage

HTML_PARSER = 'html.parser'

main_html_page = getPage()
main_page_dom = BeautifulSoup(main_html_page, HTML_PARSER)

for zoo_link in main_page_dom.find_all('a'):
    zoo_link_href = zoo_link.get('href')
    print(zoo_link_href)
    zoo_page_dom = BeautifulSoup(getPage(zoo_link_href), HTML_PARSER)
    

