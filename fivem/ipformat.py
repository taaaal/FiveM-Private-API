import socket 

from socket import gaierror 
from fivem.errors import BadIPFormat

class ServerIPValidator:
  
    def __init__(self):
        self._error = BadIPFormat('[ERROR] Incorrect IP format.')
        self._default_port = 30120
  
    def convert(self, argument):
        
        if argument.startswith(('fivem', 'www')):
            try:
                argument = socket.gethostbyname(argument)
            except gaierror:
                raise self._error
      
        def is_valid_ip(ip):
            octets = ip.split('.')
            return len(octets) == 4 and \ 
                   all(octet.isdigit() and 0 <= int(octet) <= 255 for octet in octets)
        
        def is_valid_port(port):
            return port.isdigit() and len(port) in (4, 5)
                
        try:
            ip, port = argument.split(':')
        except ValueError:
            port = self._default_port
        finally:
            is_valid = is_valid_ip(ip) and is_valid_port(port)
            if not is valid: 
                raise self._error
            converted = '{0}:{1}'.format(ip, port)
            return converted 
