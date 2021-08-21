#
#   Main class to handle incomming connections blocking
#   @levkany.dev
#

import os, sys

class Blacklist():

    #   initialize the default properties
    def __init__(self):
        self.collection = set()



    #
    #   loads blacklist file
    #
    def load_config(self, filepath:str=''):
        try:
            with open(filepath, 'r') as data:
                data_buffer = data.read()
                data_buffer = data_buffer.split('\n')
                self.collection = set(data_buffer)
            return True

        # [ERROR] - No such file or directory
        except(FileNotFoundError):
            return False


    #
    #   adds a new ip to the blacklist collection
    #
    def deny(self, ip:str=''):
        self.collection.add(ip)
        return True



    #
    #   removes an ip from the blacklist collection
    #
    def remove(self, ip:str=''):
        for index, item in enumerate(self.collection):
            if(item == ip):
                self.collection.remove(ip)
                return True
        return False



    #
    #   check if ip exists in the blacklist collection   
    #
    def find(self, ip:str=''):
        return ip in self.collection
        
