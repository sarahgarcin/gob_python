import tweepy
import random
import os
import pickle
from dotenv import load_dotenv
from dateutil import parser

load_dotenv()
consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

infile = open('value','rb')
bitcoin_data = pickle.load(infile)
infile.close()

print(bitcoin_data)

date_bitcoin = parser.parse(bitcoin_data["timestamp"])

api = tweepy.API(auth)

tweets_by_date = []
print(date_bitcoin.date())

for tweet in tweepy.Cursor(api.user_timeline, screen_name="@closerfr").items(200):
    if  date_bitcoin.date() == tweet.created_at.date():
        tweets_by_date.append(tweet.id)

print(tweets_by_date)
tweet_id = random.choice(tweets_by_date)
tweet_url = "https://twitter.com/closerfr/status/" + str(random.choice(tweets_by_date))

debuts = [
    {
        "type": "vb",
        "tournure": "Tout ça alors que",
    },
    {
        "type": "vb",
        "tournure": "Suite à quoi",
    },
    {
        "type": "vb",
        "tournure": "Pendant ce temps,",
    },
    {
        "type": "vb",
        "tournure": "Et tout à coup",
    },
    {
        "type": "vb",
        "tournure": "On comprend pourquoi",
    },
    {
        "type": "vb",
        "tournure": "Soudainement",
    },
    {
        "type": "vb",
        "tournure": "Au même moment,",
    },
    {
        "type": "vb",
        "tournure": "Et comme par hasard,",
    },
    {
        "type": "vb",
        "tournure": "Avec tout ça",
    },
    {
        "type": "nom",
        "tournure": "Une explication à",
    },
    {
        "type": "nom",
        "tournure": "Sans doute un lien avec",
    },
    {
        "type": "nom",
        "tournure": "Ça explique",
    },
    {
        "type": "nom",
        "tournure": "Plus de mystère quant à",
    },
    {
        "type": "nom",
        "tournure": "Enfin la lumière sur",
    }
]

ponctuations = [".", " !", "...", " ?"]

tournure = random.choice(debuts)
ponctuation = random.choice(ponctuations)

if tournure["type"] == "vb":
    if bitcoin_data['drop']:
        info_bitcoin = "le bitcoin a baissé de"
    else: 
        info_bitcoin = "le bitcoin a augmenté de"
elif tournure["type"] == "nom":
    if bitcoin_data['drop']:
        info_bitcoin = "la baisse du bitcoin de"
    else: 
        info_bitcoin = "la hausse du bitcoin de"

taux = str(round(bitcoin_data['abs_change_percent_7d'],2)) + "%"
info_bitcoin = info_bitcoin + " " + taux

final_tweet = tournure["tournure"] + " " + info_bitcoin + ponctuation + " " + tweet_url

print(final_tweet)

api.update_status(final_tweet)
