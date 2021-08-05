from PyAPI.class_http_responder import HttpResponder

#
# recieved params:
# client:str - this is the client ip which initiated the request
# method:str - this is request method, aka: GET/POST..
# path:str   - this is the request resource path
# body:str   - this is the request query string or Body data (depending on the request method) 
#
def callback(data):
        #
        # Example data:
        # {'client': '127.0.0.1', 'method': 'GET', 'path': '/clients/add', 'body': 'hi=hello%20world'}
        #

        # The responder accepts the following aguments:
        #  status_code:int = 200                - the status code to responde with
        #  data:str|dict = empty dict           - the data to send to back to the request initiator
        #  overrides:dict = empty dict          - overrides the responde headers
        return HttpResponder.build(200, 'New clients/add callback', {'Content-type': 'text/html'})