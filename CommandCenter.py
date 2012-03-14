'''
Created on 10 Mar 2012

@author: freynaud
'''
import http.server
import urllib.parse
import json
import subprocess
import socketserver
from SnapshortRevertedListener import SnapshotListener
import LinuxNetworkInterface
import time
import sys
import http.client, urllib.parse
import json



    
    
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
        
        
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
        print(post_data)
        self.send_response(200, "success")
        self.end_headers()
        #self.wfile.write(b)
     

def no_op():
    print("no op")





def get_mac_address():
    return sys.argv[1]


def send_ok (ip):
    body = json.dumps({"cmd":"NodeWokeUpEvent", "content" :{"mac":get_mac_address() , "ip":ip}})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = http.client.HTTPConnection("192.168.216.133:4444")
    conn.request("POST", "/grid/admin/NodeCommandCenterServlet/", body, headers)
    response = conn.getresponse()
    print(response.status, response.reason)
    data = response.read()
    print(data)
    conn.close()


def wait_for_ip():
    # expecting the mac address of the interface to use as the only parameter for that script.
    interface = LinuxNetworkInterface.LinuxNetworkInterface(get_mac_address())
    if (not interface.is_up()):
        interface.mark_up()
    
    while not interface.get_ip_v4():
        ip = interface.get_ip_v4()
        if (ip):
            send_ok(ip)            
        else :
            print("waiting")
            time.sleep(1)

      
if __name__ == '__main__':
    
    #send_ok("the ip")
    listener = SnapshotListener(callback=wait_for_ip)
    listener.start()
    
    PORT = 5556
    Handler = MyHandler
    httpd = socketserver.TCPServer(('', PORT), Handler)
    httpd.serve_forever()
