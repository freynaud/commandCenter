'''
Created on 10 Mar 2012

@author: freynaud
'''
import http.server
import socketserver
import urllib.parse
import json
import subprocess
from subprocess import CalledProcessError
from pickle import FALSE



class NetworkInterface:
    _interface = None
    _mac_address = None
    
    def __init__(self, mac_addres):
        self._mac_address = mac_addres
        self._eth = self._get_interface()
        
    def exist(self) :
        try:
            subprocess.check_output(["ifconfig", self.eth])
            return True
        except OSError as err:
            print(err)
            return True 
        except CalledProcessError as err:
            print(err)
            return False
        
        
    def _get_interface(self):
        res = self._get_hwaddr_linel()
    
    def is_up(self):
        res = self._get_inet_addr_line()
        return 'inet addr' in res
    
    def get_ip(self):
        line = self._get_inet_addr_line()
        prefix = "inet addr:"
        start = line.index(prefix) + len(prefix)
        end = line.find(" ",start)
        res = line[start:end]
        return res
    
    def mark_up(self):
        try:
            subprocess.check_output(["ifconfig", self.eth, "up"])
            return True
        except CalledProcessError as err:
            print(err)
            return False
    
    def _get_inet_addr_line(self):
        if ( self.exist() == False):
            print("error")
        else:
            ifconfig = ["ifconfig", self.eth ]
            grab_ip = ["grep", "inet addr"]
            p1 = subprocess.Popen(ifconfig, stdout=subprocess.PIPE)
            p2 = subprocess.Popen(grab_ip, stdin=p1.stdout, stdout=subprocess.PIPE)
            p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
            output = p2.communicate()[0]
            res =  output.decode("UTF-8")
            return res

    def _get_hwaddr_linel(self):
        ifconfig = ["ifconfig", "-a"]
        grab_hwaddr= ["grep", "HWaddr"]
        p1 = subprocess.Popen(ifconfig, stdout=subprocess.PIPE)
        p2 = subprocess.Popen(grab_hwaddr, stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
        output = p2.communicate()[0]
        res =  output.decode("UTF-8")
        return res
    
    
    
    
class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print(self)
       
        res = urllib.parse.urlparse(self.path)
        query = res[4];
        params = urllib.parse.parse_qs(query)
        j = params['json']
        b = bytes("<html><body>default</body></html>\n", "UTF-8"); 
        if (j):
            param = j[0]
            print(param)
            j = json.loads(param)
            print(json.dumps(j, sort_keys=True, indent=4))
            command = j['cmd']
            try:
                b = subprocess.check_output(command)
            except OSError as err:
                print(err)
                b = bytes(err.strerror, "UTF-8"); 
        else:
            print("error, no json param")
        
        self.send_response(200, "success")
        self.end_headers()
        self.wfile.write(b)
        
         
if __name__ == '__main__':
    PORT = 8081
    
    eth0 = NetworkInterface("00:0c:29:cd:ad:02")
    print(eth0.exist())
    print(eth0.is_up())
    print(eth0.get_ip())
    print(eth0.mark_up())
    
    #Handler = MyHandler
    #httpd = socketserver.TCPServer(('', PORT), Handler)
    #httpd.serve_forever()
