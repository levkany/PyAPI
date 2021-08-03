from class_server import RestServer
from class_endpoints import RestEndPoints
from class_http_responder import HttpResponder

# import endpoint callbacks
from endpoints.clients import clients, clients_add

# override 404 not found callback
def __not_found_callback():
    return HttpResponder.build(404, '<h1>This API endpoint is not found!</h1>', {'Content-type': 'text/html'})

# initialize endpoints handler
endpoints = RestEndPoints(not_found_callback=__not_found_callback)

# add some endpoints
endpoints.add('/clients', clients.GET, clients.POST)
endpoints.add('/clients/add', clients_add.GET, clients_add.POST)

# start the server
server = RestServer('192.168.1.15', endpoints=endpoints, env='local')
server.start()