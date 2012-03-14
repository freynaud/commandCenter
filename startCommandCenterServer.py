'''
Created on 10 Mar 2012

@author: freynaud
'''
import http.server
import urllib.parse
import json
import subprocess
import socketserver
    
    
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
     


if __name__ == '__main__':
    PORT = 5558
    Handler = MyHandler
    httpd = socketserver.TCPServer(('', PORT), Handler)
    httpd.serve_forever()
