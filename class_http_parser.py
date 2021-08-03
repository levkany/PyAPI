#
#   Main class to parse a raw http request
#   @levkany.dev
#

class HttpParser():

    #   initialize the default properties
    def __ini__(self, raw_data:str=''):
        self.raw_data = raw_data
      


    #
    #   Return the parsed version of the raw http data
    #
    @staticmethod
    def parse(raw_data):
        # if(False == raw_data): return None
        lines = str(raw_data, 'utf-8').split('\r\n')
        # return lines
        parsed_data = {}
        index = 0
        for line in lines:

            # request type / uri / version
            if(0 ==index):
                header_1 = line.split(' ')
                parsed_data['method'] = header_1[0]
                parsed_data['uri'] = header_1[1]
                parsed_data['version'] = header_1[2]

                # update uri and get query string
                if('GET' == parsed_data['method']):
                    try:
                        parsed_data['query_string'] = header_1[1].split('?')[1]
                        parsed_data['uri'] = header_1[1].split('?')[0]
                    except: None

                # remove trailing backslash of the uri
                if(parsed_data['uri'].endswith('/')):
                    parsed_data['uri'] = parsed_data['uri'][:-1]

            # body data
            if(index == (lines.__len__() -1) and '' != line):
                parsed_data['body'] = line
            index+=1
        return parsed_data