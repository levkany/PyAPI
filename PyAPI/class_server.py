#
#   Main class to handle the rest api server
#   @levkany.dev
#

import socket
import threading
import time
from PyAPI.class_http_parser import HttpParser
from PyAPI.class_blacklist import Blacklist
import random

class RestServer():

    #   initialize the default properties
    #   note: by default, if no lan device's ip is passed, the socket wont be able to accept connections from the outter world
    #   note: by default the endpoint port is 8820, it is adviced to leave it as it is
    def __init__(self, local_ip:str = '127.0.0.1', local_port:int = 8820, endpoints=list, env:str=''):

        self.local_ip                   = local_ip
        self.local_port                 = local_port
        self.backlog                    = 0
        self.attached_endpoints         = endpoints
        self.connected_clients          = []
        self.env                        = env
        self.is_env_local               = self.env == 'local'

        # initialize blacklist handler
        self.blacklist                  = Blacklist()

    

    #
    #   Returns the server port
    #
    def get_port(self):
        return self.local_port



    #
    #   Sets a new server port
    #
    def set_port(self, new_port:int):
        self.local_port = new_port



    #
    #   Returns the server ip address
    #
    def get_ip(self):
        return self.local_ip



    #
    #   Sets a new server ip address
    #
    def set_ip(self, new_ip:int):
        self.local_ip = new_ip



    #
    #   Returns the number of allowed quoted connections
    #
    def get_backlog(self, maxmimum:int):
        return self.backlog



    #
    #   Sets the number of allowed quoted connections
    #
    def set_backlog(self, maxmimum:int):
        self.backlog = maxmimum



    #
    #   Setup and bind the server socket
    #   note: currently the server doesn't support IPv6
    #
    def setup(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.local_ip, self.local_port))



    #
    #   Starts to listen for incomming connections
    #
    def start(self):
        self.setup()
        self.server.listen(self.backlog)
        while(True):

            # accept connections and move to unique thread to prevent long running operations to block any future or backloged connections
            client, address = self.server.accept()

            # deny connections if ip is in the blacklist
            if self.blacklist.find(address[0]):
                client.close()
                continue
            
            if(self.is_env_local):
                if(address[0] not in self.connected_clients):
                    self.connected_clients.append(address[0])
                    client_thread = threading.Thread(target=self.client_thread, args=(client, address, client.recv(204800)))
                    client_thread.start()
            else:
                client_thread = threading.Thread(target=self.client_thread, args=(client, address, client.recv(204800)))
                client_thread.start()



    #
    #   Unlock an ip to allow communications
    #   Used in local enviroment to prevent duplicated packets reaching the listener
    #
    def unlock_ip(self, ip:str):
        self.connected_clients.remove(ip)



    #
    #   Backgronud thread to handle client request
    #
    def client_thread(self, client, address, data):
        parsed = HttpParser.parse(data)
        method=parsed['method']
        path=parsed['uri']
        body = ''
        try:
            body = parsed['query_string']
        except:
            try:
                body = parsed['body']
            except: body = ''

        # empty path is the default path
        if('' == path): path = '/'

        # find a match between the request method and the registered endpoint
        # also match the request method to the registered endpoint supported method

        is_callback_found = False
        for endpoint in self.attached_endpoints.get_all_endpoints():
            endpoint_path = endpoint[0]
            
            # dyanmic endpoint handle
            if(':' in endpoint_path):
                raw_subpoints = endpoint_path[endpoint_path.index('/', 1) + 1:]
                endpoint_path = endpoint_path[0:endpoint_path.index('[', 1) -1]
                subpoints = raw_subpoints.split('/')

                # check if the extracted dynamic path exists in the requested path
                # first find the path without the dynamic subpaths so that we can compare it
                new_path = ''
                try:
                    new_path = '/'.join(path.split('/')[0:subpoints.__len__()])
                except: pass

                if('' != new_path):
                    if(endpoint_path == new_path):

                        # attach each dynamic path the id defined by the user
                        subpaths = path.split('/')[endpoint_path.split('/').__len__():]
                        subpath_ids = raw_subpoints[raw_subpoints.index('['):].split('/')

                        # make sure the dynamic paths count matching the registered count
                        if(subpaths.__len__() == subpath_ids.__len__()):
                            subpoints = {}
                            for index, id in enumerate(subpath_ids):
                                subid = id[id.index(':') +1 :id.index(']')]
                                subpoints[subid] = subpaths[index]


                            is_callback_found = True
                            method_callback = endpoint[1]
                            data_to_send = bytearray(method_callback({'client': address[0], 'data': parsed, 'subpaths': subpoints}), 'utf-8')
                            try:
                                client.send(data_to_send)
                            except: is_callback_found = False
            
            # static endpoint handle
            else:
                if(endpoint_path == path):
                    is_callback_found = True
                    method_callback = endpoint[1]
                    data_to_send = bytearray(method_callback({'client': address[0], 'data': parsed}), 'utf-8')
                    try:
                        client.send(data_to_send)
                    except: is_callback_found = False

        if(False == is_callback_found):
            # data can be empty / False - if no 404 callback is registered
            data_to_send = self.attached_endpoints.endpoint_not_found()
            client.send(bytearray(data_to_send, 'utf-8'))

        # always close the client connection after each request
        client.close()

        # wait a bit before unlocking the ip
        if(self.is_env_local):
            time.sleep(1)
            self.unlock_ip(address[0])
        return False



    #
    #   add ip to blacklist and deny service from that ip
    #
    def deny(self, ip:str=''):
        return self.blacklist.deny(ip)
            

    #
    #   loads blacklist file and auto blacklist the ip's in the file
    #
    def load_blacklist(self, filepath:str=''):
        return self.blacklist.load_config(filepath)
            