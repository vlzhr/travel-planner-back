try:
    from urllib2 import urlopen
except Exception:
    from urllib.request import urlopen
import json
from codecs import open
from random import randint
import os


dests_file = os.path.join(os.path.dirname(__file__), "dests.json")

def read_dests_file():
    with open(dests_file, encoding="utf-8") as f:
        return json.loads(f.read())
def write_dests_file(content):
    with open(dests_file, "w", encoding="utf-8") as f:
        f.write( json.dumps(content) )
    return ""

def load_dest_info(fr, to):
    link = "http://min-prices.aviasales.ru/calendar_preload?origin=" + fr + "&destination=" + to + "&one_way=true&depart_date=2018-08-15"
    text = urlopen(link).read().decode("utf-8")
    data = json.loads(text)
    try:
        if not len(data['best_prices']):
            return {"price": 0, "distance": 0}
    except Exception:
        return {"price": 0, "distance": 0}
    
    prices = [n['value'] for n in data['best_prices']]
    price = prices[int( len(prices) / 2 )]
    distance = data['best_prices'][0]["distance"]
    return {"price": price, "distance": distance}

def get_dest_info(fr, to):
    fr, to = fr.upper(), to.upper()
    return load_dest_info(fr, to)
##    dests = read_dests_file()
##    if fr in dests:
##        if to in dests[fr]:
##            return dests[fr][to]
##    else:
##        dests[fr] = {}
##    dests[fr][to] = load_dest_info(fr, to)
##    write_dests_file(dests)
##    return dests[fr][to]

def find_iata(q):
    link = "http://autocomplete.travelpayouts.com/places2?term=" + q + "&locale=ru,en&types[]=city"
    text = urlopen(link).read().decode("utf-8")
    data = json.loads(text)
    data = [[n["name"], n["code"]] for n in data]
    return data[:4]

def pot_test(ra):
    link = os.path.join(os.path.dirname(__file__), "pot.json")
    with open(link, "w", encoding="utf-8") as f:
        f.write( json.dumps(ra) )



