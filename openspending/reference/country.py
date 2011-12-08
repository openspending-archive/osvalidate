from openspending.reference.util import get_csv

data = get_csv('countries')
conv = lambda c: (c['ISO 3166-1 2 Letter Code'].decode('utf-8'), 
                  c['Common Name'].decode('utf-8'))
COUNTRIES = dict(map(conv, data))

