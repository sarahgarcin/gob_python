import tweepy
import random
from dateutil import parser

consumer_key = ""
consumer_secret = ""

access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

bitcoin_data = {
    'value': 46214.40976784179, 
    'abs_change_percent': 1.34283373, 
    'drop': False, 
    'timestamp': '2021-04-21T13:31:14.956Z', 
    'abs_change_percent_7d': 15.06953104
}

date_bitcoin = parser.parse(bitcoin_data["timestamp"])

api = tweepy.API(auth)

tweets_by_date = []

for tweet in tweepy.Cursor(api.user_timeline, screen_name="@closerfr").items(200):
    if  date_bitcoin.date() == tweet.created_at.date():
        tweets_by_date.append(tweet.id)

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

taux = str(bitcoin_data['abs_change_percent_7d']) + "%"
info_bitcoin = info_bitcoin + " " + taux

final_tweet = tournure["tournure"] + " " + info_bitcoin + ponctuation + " " + tweet_url

print(final_tweet)
