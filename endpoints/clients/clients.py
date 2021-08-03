from class_http_responder import HttpResponder

def GET(data):
        # Do something and return
        return HttpResponder.build(507, {"whichEndPoint": "endpoint of GET"}, {'Content-type': 'application/json'})

def POST(data):
        # Do something and return
        return HttpResponder.build(200, 'endpoint of POST')

def DELETE(data):
        # Do something and return
        return HttpResponder.build(200, 'endpoint of DELETE')

def PUT(data):
        # Do something and return
        return HttpResponder.build(200, 'endpoint of PUT')