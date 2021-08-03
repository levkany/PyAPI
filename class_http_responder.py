#
#   Main class to build a raw http syntax (response)
#   @levkany.dev
#

import json
from class_http_codes import HttpCodes

class HttpResponder():

    #   initialize the default properties
    def __ini__(self):
        return None


    #
    #   Return the parsed version of the raw http data
    #   Notes: data param can be of type: STR/DICT
    #
    @staticmethod
    def build(status_code:int=200, data=False, overrides:dict={}):

        # convert data to json string if it is a dict
        if(dict == type(data)):
            data = json.dumps(data)


        # prepare defaults
        parsed_data = dict()
        parsed_data['HTTP'] = '1.1 '+ str(status_code)
        parsed_data['content-language'] = 'en-US'
        parsed_data['content-length'] = data.__len__()
        parsed_data['content-type'] = 'text/html; charset=UTF-8'
        parsed_data['data'] = str(data)

        print(parsed_data)

        # add / override headers based on passed ones
        if(False != overrides):
            for key in overrides:
                parsed_data[str(key).lower()] = overrides[key]

        # build raw string and return
        opt = ''
        for key in parsed_data:
            if('HTTP' == key):
                opt += 'HTTP/' + str(parsed_data[key]) + ' ' + HttpCodes.get(status_code)['msg'] + '\r\n'
            elif('data' == key):
                opt += '\r\n' + str(parsed_data[key])
            else:
                opt += str(key) + ': ' + str(parsed_data[key]) + '\r\n'

        return opt