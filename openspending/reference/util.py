import os
import json

def get_resource(name):
    path = os.path.dirname(__file__)
    fh = open(os.path.join(path, 'data', name), 'r')
    return fh

def get_json(name):
    fh = get_resource(name + '.json')
    data = json.load(fh)
    fh.close()
    return data


