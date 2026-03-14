from bs4 import BeautifulSoup
import requests


DOMAIN = "https://django-anuncios.solyd.com.br"
URL_AUTOMOBILES = "https://django-anuncios.solyd.com.br/automoveis/"


def search(url):
    try:
        aux_request = requests.get(url)
        
        if aux_request.status_code == 200:
            return aux_request.text
        else:
            print("\tError making request!") 

    except Exception as error:
        print("\tError making request!")
        print(error)


def parsing(var_to_parsing):
    try:
        aux_soup = BeautifulSoup(var_to_parsing, "html.parser")

        return aux_soup
    
    except Exception as error:
        print("\tError making html parsing!")
        print(error)


def finding_links(soup_param):
    superClass = soup_param.find("div", class_="ui three doubling link cards")
    cards = superClass.find_all("a")

    links_aux = []
    for card in cards:
        link = card["href"]
        links_aux.append(link)
    
    return links_aux


if __name__ == "__main__":
    var_request = search(URL_AUTOMOBILES)

    if var_request:
        soup = parsing(var_request)

        if soup:
            links = finding_links(soup)
            print(links)
        
