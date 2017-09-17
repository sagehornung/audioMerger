import requests

def http_post_request():
    payload = {'lat': 36.78848171840966, 'lng': -121.82906786028143, 'id': '1'}
    headers = {'content-type': 'application/json'}
    r = requests.post("http://localhost:4200/update", payload, headers)
    print(r.status_code, r.reason)
    return r.status_code1

# print http_post_request()


import json
import urllib2

payload = {'lat': 36.78848171840966, 'lng': -121.82906786028143, 'id': '1'}

req = urllib2.Request('http://localhost:4200/update')
req.add_header('Content-Type', 'application/json')

response = urllib2.urlopen(req, json.dumps(payload))
print response