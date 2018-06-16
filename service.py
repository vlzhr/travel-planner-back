import os
from codecs import open
from json import dumps,loads

def link(*args):
    return os.path.join(os.path.dirname(__file__), *args)

def load_file(*name):
    with open(link(*name), "r", encoding='utf-8') as f:
        return loads(f.read())

def dump_to_file(dic, *name):
    with open(link(*name), "w", encoding='utf-8') as f:
        return f.write(dumps(dic)) 
