import requests
import random

#
#   Endpoint tests
#

# x = requests.delete('http://192.168.1.15:8820?hello"=world!', data={'param1': 'delete = this and that', 'param22': 'remove at all and ALL!! !! !'})
# x = requests.post('http://192.168.1.15:8820/clients/', data={'param1': 'delete = this and that', 'param22': 'remove at all and ALL!! !! !'})
# x = requests.get('http://192.168.1.15:8820/clients/add?hello=world')
# x = requests.get('http://192.168.1.15:8820/clients/notfoundcallback?hello=world')
# x = requests.get('http://192.168.1.15:8820/clients?redirect=123123')


#
#   Pending connection tests
#

# for x in range(100):
#     data = requests.get('http://localhost:8820/' + str(random.random()))
#     print(data)


#
#   File upload test
#

# files = {'upload_file': open('./test.pdf','rb'), 'upload_file_2': open('./file_2.txt','rb')}
# x = requests.post('http://localhost:8820/', files=files, data={'username': 'hello world user', 'password': 'hello world pass!'})
# print(x)


# str1 = ''

# for index, item in enumerate(str1.split('\r\n')):
#     print('* ' + str(index) + ' - ' + item)