#
#   Main class to handle the rest api server
#   @levkany.dev
#

import socket
import threading
import time
from class_http_parser import HttpParser

class RestServer():

    #   initialize the default properties
    #   note: by default, if no lan device's ip is passed, the socket wont be able to accept connections from the outter world
    #   note: by default the endpoint port is 8820, it is adviced to leave it as it is
    def __init__(self, local_ip:str = '127.0.0.1', local_port:int = 8820, endpoints=list, env:str=''):
        self.local_ip = local_ip
        self.local_port = local_port
        self.attached_endpoints = endpoints
        self.connected_clients = []
        self.env = env
        self.is_env_local = self.env == 'local'

    

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
    #   Setup and bind the server socket
    #   note: currently the server doesn't support IPv6
    #
    def setup(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.local_ip, self.local_port))



    #
    #   Starts to listen for incomming connections
    #
    def start(self):
        self.setup()
        self.server.listen()
        while(True):

            # accept connections and move to unique thread to prevent long running operations to block any future or backloged connections
            client, address = self.server.accept()
            
            if(self.is_env_local):
                if(address[0] not in self.connected_clients):
                    self.connected_clients.append(address[0])
                    client_thread = threading.Thread(target=self.client_thread, args=(client, address, client.recv(1024)))
                    client_thread.start()
            else:
                client_thread = threading.Thread(target=self.client_thread, args=(client, address, client.recv(1024)))
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

        # find a match between the request method and the registered endpoint
        # also match the request method to the registered endpoint supported method

        is_callback_found = False
        for endpoint in self.attached_endpoints.get_all_endpoints():
            endpoint_path = endpoint[0]
            if(endpoint_path == path):
                # find the proper method to invoke from the endpoint
                for method_callback in endpoint[1]:
                    
                    # matched callback!
                    if(method_callback.__name__ == method):
                        is_callback_found = True
                        data_to_send = bytearray(method_callback(data), 'utf-8')
                        try:
                            client.send(data_to_send)
                        except: is_callback_found = False
                        
                break

        if(False == is_callback_found):
            # data can be empty / False - if no 404 callback is registered
            data_to_send = self.attached_endpoints.endpoint_not_found()
            client.send(bytearray(data_to_send, 'utf-8'))

        print('sent response to client')

        # always close the client connection after each request
        client.close()

        # wait a bit before unlocking the ip
        if(self.is_env_local):
            time.sleep(1)
            self.unlock_ip(address[0])
        return False