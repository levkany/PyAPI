from io import FileIO
from PyAPI.class_http_responder import HttpResponder

#
# recieved params:
# client:str    - this is the client ip which initiated the request
# data:dict     - contains all the informations parsed by the server including params, files, uri, etc
#
def callback(data):
        #
        # Updated Example data:
        # {'client': '127.0.0.1', 'data': {'body': [], 'files': [], 'method': 'GET', 'uri': '/clients', 'version': 'HTTP/1.1', 'query_string': [{'name': 'redirect', 'value': '123123'}]}}
        #

        if(data['data']['files'].__len__()):
                for file in data['data']['files']:
                        with open('./uploads/' + file['filename'], 'xb') as handler:
                                handler.write(file['binary'])

        # The responder accepts the following aguments:
        #  status_code:int = 200                - the status code to responde with
        #  data:str|dict = empty dict           - the data to send to back to the request initiator
        #  overrides:dict = empty dict          - overrides the responde headers
        return HttpResponder.build(200, 'clients home callback', {'Content-type': 'text/html'})