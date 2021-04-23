import pickle
from functools import reduce
from dotenv import load_dotenv
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import os 

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

filename = 'value'

def data_check_and_clear():
  try:
    infile = open(filename,'rb')
    value = pickle.load(infile)
    infile.close()
  except EOFError as err:
    print(err)
    value = {
      "value": '',
      "abs_change_percent": '',
      "abs_change_percent_7d": '',
      "drop": '',
      "timestamp": ''
    }
    outfile = open(filename,'wb')
    pickle.dump(value, outfile)
    outfile.close()

def biggest_day(day1, day2):
  if day1["abs_change_percent"] > day2["abs_change_percent"]:
    return day1
  else:
    return day2

def fetch_7d_change():
  session = Session()
  session.headers.update(headers)
  try:
      response = session.get(url, params=parameters)
      d = response.json()
      for x in d['data']:
        return abs(x['quote']['EUR']['percent_change_7d'])
      
  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

data_check_and_clear()

listfile = open('weekly_list','rb')
weekly_list = pickle.load(listfile)
listfile.close()
day = reduce(biggest_day,weekly_list)
day['abs_change_percent_7d'] = fetch_7d_change()

valuefile = open('value','wb')
pickle.dump(day, valuefile)

print(day)