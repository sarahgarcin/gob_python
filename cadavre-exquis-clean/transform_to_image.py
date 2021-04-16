import transform_text
from google_images_search import GoogleImagesSearch
import sys
import os
import random

newText = transform_text.newText
folder_path = './static/images/'
image_path = './static/images/image.jpg'

common_word_list= ['à','je', 'tu', 'il', 'elle', 'on', 'nous', 'vous', 'ils', 'elles','me', 'te', 'le', 'lui', 'la', 'les', 'leur', 'eux', 'moi', 'toi', 'celui', 'celle', 'ceux', 'celles', 'ceci', 'cela', 'ce', 'ça', 'celui-ci','qui', 'que', 'quoi', 'dont', 'où','aussi' ,'le' ,'la','un', 'une', 'du', 'de', 'de la', 'des' , 'les', 'ce', 'cet', 'cette', 'mon', 'ton', 'son', 'notre', 'votre', 'leur', 'mes', 'ses', 'tes']

def determine_common_word(word_to_check: str):
	for common_word in common_word_list:
		if common_word == word_to_check:
			return True
	return False

def text_to_keyword(txt: str):
	sentence = txt.split()
	sentence[:] = [word for word in sentence if not determine_common_word(word)]
	return sentence

def get_google_image(folder, image, newText):
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

	if os.path.exists(image):
		os.remove(image)
	else:
		print("The file does not exist")

	for image in gis.results(): 
		image.download(folder)
		image.resize(500, 500)

#get_google_image(folder_path, image_path, newText)

