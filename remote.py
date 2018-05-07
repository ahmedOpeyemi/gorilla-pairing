import requests


def getPage(route="USAmenu.htm"):

    cookies = {
        '_c': 'y',
    }

    headers = {
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
    }

    base_url = "http://www.dewarwildlife.org/jrdavis-gorilla-studbook/"

    response = requests.get(
        "{base_url}{route}".format(base_url=base_url, route=route),
        headers=headers,
        cookies=cookies
    )

    return response.content
