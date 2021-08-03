import requests
x = requests.delete('http://192.168.1.15:8820?hello"=world!', data={'param1': 'delete = this and that', 'param22': 'remove at all and ALL!! !! !'})
x = requests.post('http://192.168.1.15:8820/clients/', data={'param1': 'delete = this and that', 'param22': 'remove at all and ALL!! !! !'})
x = requests.get('http://192.168.1.15:8820/clients/add?hello=world')
x = requests.get('http://192.168.1.15:8820/clients/notfoundcallback?hello=world')
x = requests.get('http://192.168.1.15:8820/clients?redirect=123123')