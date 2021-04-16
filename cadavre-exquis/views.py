from flask import Flask
from flask import url_for
from flask import render_template
from flask_caching import Cache

# On importe la fonction 'get' (téléchargement) de 'requests'
# Et la classe 'Selector' (Parsing) de 'scrapy'
from requests import get
from scrapy import Selector
import re
import w3lib.html
import random 
import sys
import os
from google_images_search import GoogleImagesSearch


config = {
    "DEBUG": True, 
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)
app.static_folder = 'static'

app.config.from_mapping(config)
cache = Cache(app)

@app.route("/")

def hello():
   # choice = input("Que souhaitez-vous rechercher ? Tapez 0 pour un contenu au hasard.\n"">>> ")
    text = None

    # Lien de la page à scraper
    #  if choice == "0":
    #  url = "https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard"
    #   else:
    # url = "https://fr.wikipedia.org/wiki/" + choice

    # url = "https://fr.wikipedia.org/wiki/Al-K%C3%A2mil"

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

    if text is None:
        print("Erreur")
    else:
        print(text)


    # text = "Loin du cliché de l’agent d’État vivant à l’abri des vicissitudes de l’existence, les hauts fonctionnaires japonais travaillent dans des conditions éprouvantes, effectuant jusqu’à trois cents heures supplémentaires par mois. Les lois sociales — déjà très peu protectrices — ne s’appliquent pas à ces salariés. Un nombre croissant d’entre eux désertent les ministères, provoquant une crise inédite."

    newText = text.lower()

    replacements = ["wsh", "bref", "genre", "mdr", "ptdr", "jpp"]

    print(replacements)

    def randomponctuation(match):
        ponctuation = random.choice(replacements)
        length = random.randint(0, 6)
        if length == 1:
            length = 0
        if ponctuation == "mdr":
            ponctuation = ponctuation + length*"r"
        if ponctuation == "jpp":
            ponctuation = ponctuation + length*"p"
        print(match.group())
        if match.group() == "," or match.group() == ".":
            ponctuation = " " + ponctuation
        return ponctuation

    def randompoints(match):
        length = random.randint(4, 10)
        string = "." * length
        return string

    newText = re.sub("[,;:!?—]", randomponctuation, newText)
    newText = re.sub("(?<!\.)\.(?!\.)", randomponctuation, newText)
    newText = re.sub("\.\.\.", randompoints, newText)
    newText = re.sub("[()\"]|(« | »)", "", newText)
    newText = re.sub("c(’|')est", "c", newText)

    print(newText)


    imageUrl = './static/images/'

    def determine_common_word(word_to_check: str):
        for common_word in common_word_list:
            if common_word == word_to_check:
                return True
        return False

    def text_to_keyword(txt: str):
        sentence = txt.split()
        sentence[:] = [word for word in sentence if not determine_common_word(word)]
        return sentence

    common_word_list= ['à','je', 'tu', 'il', 'elle', 'on', 'nous', 'vous', 'ils', 'elles','me', 'te', 'le', 'lui', 'la', 'les', 'leur', 'eux', 'moi', 'toi', 'celui', 'celle', 'ceux', 'celles', 'ceci', 'cela', 'ce', 'ça', 'celui-ci','qui', 'que', 'quoi', 'dont', 'où','aussi' ,'le' ,'la','un', 'une', 'du', 'de', 'de la', 'des' , 'les', 'ce', 'cet', 'cette', 'mon', 'ton', 'son', 'notre', 'votre', 'leur', 'mes', 'ses', 'tes']

    txt_l = text_to_keyword(newText)
    txt_l_len = len(txt_l)

    print(txt_l_len, file=sys.stderr)
   

    ran_i = random.randrange(0, txt_l_len - 1)

    gis = GoogleImagesSearch('AIzaSyAUQgZTiWpy0YXdE0IJwkVCNrEdmSiNpiU', '175c210d3316ae770')

    _search_params = {
        'q': txt_l[ran_i],
        'num': 1,
        'safe': 'off',
        'fileType': 'jpg',
    }

    gis.search(search_params=_search_params, custom_image_name='image')

    if os.path.exists("./static/images/image.jpg"):
        os.remove("./static/images/image.jpg")
    else:
        print("The file does not exist")

    for image in gis.results(): 
        image.download(imageUrl)
        image.resize(500, 500)

    


    #text = ''
    #newText = ''
    #imageUrl = ''
    return render_template('home.html', text=text, newText=newText, imageUrl=imageUrl )