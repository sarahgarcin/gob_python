from flask import Flask
from flask import url_for
from flask import render_template
from flask_caching import Cache

from get_text import get_random_wiki_article
from transform_text import transform_text_wsh
import transform_to_image
from transform_to_image import get_google_image

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
def home(): 
    text = get_random_wiki_article()
    newText = transform_text_wsh(text)
    get_google_image(transform_to_image.folder_path, transform_to_image.image_path, newText)
    imageUrl = transform_to_image.image_path
    return render_template('home.html', text=text, newText=newText, imageUrl=imageUrl )

