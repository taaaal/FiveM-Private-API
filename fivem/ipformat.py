from fivem.errors import BadIPFormat

class ServerIP:
  
    def __init__(self):
        self._error = BadIPFormat('[ERROR] Incorrect IP format.')
        self._default_port = 30120
  
    def convert(self, argument):
        def is_valid_ip(ip):
            if ip.startswith(('fivem', 'www')):
                return True
            ip_parts = ip.split('.')
            if len(ip_parts) != 4:
                return False
            for part in ip_parts:
                if not part.isdigit() or not 0 <= int(part) <= 255:
                    return False
            return True
        
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
            retutj converted 
