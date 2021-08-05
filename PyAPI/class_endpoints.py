#
#   Main class to handle the endpoints of the rest api server
#   @levkany.dev
#

import endpoints.not_found_404

class RestEndPoints():

    #   initialize the default properties
    def __init__(self, not_found_callback=callable):
        self.endpoints = []
        self.not_found_callback = not_found_callback

    

    #
    #   Add a new endpoint to the collection of the endpoints
    #
    def add(self, endpoint:str='', executer=False):
        self.endpoints.append((endpoint, executer))


    
    #
    #   Returns all the registered endpoints
    #
    def get_all_endpoints(self):
        return self.endpoints



    #
    #   Callback to be called when callback endpoint cannot be found or executed
    #
    def endpoint_not_found(self):

        # 404 callback is registered
        try:
            return self.not_found_callback()

        # no default 404 callback
        except: return endpoints.not_found_404.__init__()

