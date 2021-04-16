from requests import get
from scrapy import Selector
import w3lib.html
import re

def get_random_wiki_article():
    url = "https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard"
    response = get(url)
    source = None  # Le code source de la page
    if response.status_code == 200:
        # Si la requete s'est bien passee
        source = response.text
        # print(response.url)
        # print(source)

    if source:
        selector = Selector(text=source)
        container = selector.css("div.mw-parser-output > p")

        for child in container:
            strippedHtml = w3lib.html.remove_tags(child.get())
            strippedHtml = re.sub(r"\[\d*]", "", strippedHtml)
            strippedHtml = strippedHtml.replace("\n", ' ').replace('\r', '')

            text = strippedHtml

    return text

text = get_random_wiki_article()
print(text)