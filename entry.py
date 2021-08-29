from PyAPI.class_server import RestServer
from PyAPI.class_endpoints import RestEndPoints
from PyAPI.class_http_responder import HttpResponder


# import endpoint callbacks
from endpoints.clients import clients, clients_add, clients_home


# override 404 not found callback
def __not_found_callback():
    return HttpResponder.build(404, '<h1>This API endpoint is not found!</h1>', {'Content-type': 'text/html'})


# initialize endpoints handler
endpoints = RestEndPoints(not_found_callback=__not_found_callback)


def default_endpoint(data):
    welcome_data = open('welcome.html', 'r').readlines()
    data_to_send = ''.join(welcome_data)
    return HttpResponder.build(200, data_to_send, {'Content-type': 'text/html'})


# add some endpoints
endpoints.add('/', default_endpoint)
endpoints.add('/clients', clients_home.callback)
endpoints.add('/clients/add', clients_add.callback)

# dynamic path values can be accessed via the callback's property: "data.subpaths" or from "data.path"
endpoints.add('/clients/new/[:id]/[:log_id]', clients.callback)


# initiaze the server
server = RestServer('127.0.0.1', endpoints=endpoints, env='prod')

# set maximum of allowed pending connections
server.set_backlog(0)

# load blacklist and add a few more ip's to block
server.load_blacklist('./blacklist.txt')
server.deny('127.0.0.2')
server.deny('8.8.8.8')
server.deny('11.11.11.11')

# finally, we can start the server :)
server.start()
