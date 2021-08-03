from PyAPI.class_http_responder import HttpResponder


def GET(data):
        # Do something and return
        return HttpResponder.build(200, '/clients/add endpoint of GET')

def POST(data):
        # Do something and return
        return HttpResponder.build(200, '/clients/add endpoint of POST')

def DELETE(data):
        # Do something and return
        return HttpResponder.build(200, '/clients/add endpoint of DELETE')

def PUT(data):
        # Do something and return
        return HttpResponder.build(200, '/clients/add endpoint of PUT')