import json
import os
from dotenv import load_dotenv
from datetime import datetime
from time import time
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import pickle
import sys

load_dotenv()
BTC_API_TOKEN = os.getenv('btc_api_key')

#api Params
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = { 
    'start':'1',
    'limit':'1',
    'convert':'EUR'
}

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': BTC_API_TOKEN,
}

filename = 'weekly_list'

#helper
def isPositive(number):
  if number < 0: 
    return True
  else:
    return False

def data_check_and_clear():
  try:
    infile = open(filename,'rb')
    w_data = pickle.load(infile)
    infile.close()
  except EOFError as err:
    print(err)
    w_list = []
    outfile = open(filename,'wb')
    pickle.dump(w_list, outfile)
    outfile.close()

#local weekly dict update
def update_data(r):
  d = r.json()
  for x in d['data']:
    v = x['quote']['EUR']['price']
    p = x['quote']['EUR']['percent_change_24h']
  timestamp = d['status']['timestamp']

  day = {
    "value": v,
    "abs_change_percent": abs(p),
    "drop": isPositive(p),
    "timestamp": timestamp
  }
  infile = open(filename,'rb')
  w_list = pickle.load(infile)
  infile.close()
  w_list.append(day)
  outfile = open(filename,'wb')
  pickle.dump(w_list, outfile)
  outfile.close()
  print(w_list)


#api call + update
def fetch_then_udpate():
  session = Session()
  session.headers.update(headers)
  try:
      response = session.get(url, params=parameters)
      update_data(response)
  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

data_check_and_clear()
fetch_then_udpate()



