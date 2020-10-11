from fivem.errors import BadIPFormat

class ServerIP:
  
    def __init__(self):
        self.error = BadIPFormat('[ERROR] Incorrect IP format.')
        self.default_port = 30120
  
    def convert(self, argument):
        def check_ip_format(ip, port):
            if ip.startswith(('fivem', 'www')):
                ip_status = True
            else:
                try:
                    ip_list = ip.split('.')      
                except ValueError:
                    ip_status = False
                else:
                    ip_status = True
            port_status = len(port) in (4, 5)
            if ip_status and port_status:
                return True
            else:
                return False
                
        try:
            ip, port = self.argument.split(':')
        except ValueError:
            port = self.default_port
        if check_ip_format(ip, port) is True:
            srvip = '{0}:{1}'.format(ip, port)
            return srvip
        else:
            raise self.error
