#
#   Main class to parse a raw http request
#   @levkany.dev
#

import urllib.parse

class HttpParser():

    #   initialize the default properties
    def __ini__(self, raw_data:str=''):
        self.raw_data = raw_data
      


    #
    #   Return the parsed version of the raw http data
    #
    @staticmethod
    def parse(raw_data):
        lines = bytearray(raw_data).split(b'\r\n')
        parsed_data = {}
        parsed_data['body'] = []
        parsed_data['files'] = []
        index = 0
        headers_found = False
        is_multipart = False
        headers = []
        body = []

        # split headers and body
        for index, line in enumerate(lines):
            if('' == bytearray(line).decode(errors="ignore") and False == headers_found):
                headers_found = True
                headers = lines[0:index]
            elif(headers_found):
                body = lines[index:(lines.__len__())]
                break
        
        # analyze headers
        for index, header in enumerate(headers):
            # request type / uri / version
            if(0 ==index):
                header_1 = bytearray(header).decode(errors="ignore").split(' ')
                parsed_data['method'] = header_1[0]
                parsed_data['uri'] = header_1[1]
                parsed_data['version'] = header_1[2]

                # update uri and get query string
                if('get' == parsed_data['method'].lower()):
                    try:
                        parsed_data['query_string'] = header_1[1].split('?')[1]
                        
                        # make GET query easier to access by converting it into an object
                        GETs = parsed_data['query_string'].split('&')
                        parsed_data['query_string'] = []
                        for _get in GETs:
                            key_value = _get.split('=')
                            parsed_data['query_string'].append({'name': key_value[0], 'value': key_value[1]})

                        parsed_data['uri'] = header_1[1].split('?')[0]
                    except: None

                # remove trailing backslash of the uri
                if('/' != parsed_data['uri'] and parsed_data['uri'].endswith('/')):
                    parsed_data['uri'] = parsed_data['uri'][:-1]  

            if('content-type' in bytearray(header).decode(errors="ignore").lower()):
                content_type = bytearray(header).decode(errors="ignore").lower().split(':')[1].split(';')[0]
                parsed_data['content_type'] = content_type.strip()
                if('multipart' in content_type.strip().lower()):
                    is_multipart = True

        for index, bodyItem in enumerate(body):
            
            # handle regular body
            if(False == is_multipart):
                decoded_bodyItem = bytearray(bodyItem).decode()
                if('' != decoded_bodyItem):
                    decoded_bodyItem = urllib.parse.unquote_plus(decoded_bodyItem)
                    items = decoded_bodyItem.split('&')
                    for item in items:
                        key_value = item.split('=')
                        combined = {str(key_value[0]).replace('"', ''): key_value[1]}
                        parsed_data['body'].append(combined)

            # handle multipart body
            else:
                try:
                    data = bytearray(bodyItem).decode(errors="ignore")
                    if('content-disposition' in data.lower()):
                        disposition = data.split(':')[1].split(';')
                        fieldname = fieldvalue = filename = ''
                        is_file = False
                        for item in disposition:
                            key_value = item.split('=')
                            if('name' == key_value[0].lower().strip()):
                                fieldname = key_value[1]
                            elif('filename' == key_value[0].lower().strip()):
                                filename = key_value[1]
                                is_file = True

                        # prepare the multipart body for user callback
                        if(False == is_file):
                            fieldvalue = bytearray(body[(index + 2)]).decode(errors="ignore") # fetch converted content
                            combined = {str(fieldname).replace('"', ''): fieldvalue}
                            parsed_data['body'].append(combined)
                        else:
                            try:
                                fieldvalue = body[(index + 2)] # fetch raw bytes
                                parsed_data['files'].append({
                                    'fieldname': str(fieldname).replace('"', ''),
                                    'filename': filename,
                                    'binary': fieldvalue,
                                })
                                combined = {fieldname: {
                                    'filename': filename,
                                    'binary': fieldvalue
                                }}
                                parsed_data['files'].append(combined)
                            except: pass
                except: pass
        return parsed_data