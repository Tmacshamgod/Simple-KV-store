import http.client
import json

connection = http.client.HTTPConnection('localhost', port=8080)
headers = {'Content-type': 'application/json'}
connection.request('POST', '/set/name?value=Gideon', headers=headers)

response = connection.getresponse().read()

d = json.loads(response.decode())
print('update_time = %ss' % d['update_time'])
print('data = %s' % d['data'])
print '----------------------'

connection.request('GET', '/get/name', headers=headers)

response = connection.getresponse().read()
d = json.loads(response.decode())
print('value = %s' % d['value'])
