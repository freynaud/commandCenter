'''
Created on 10 Mar 2012

@author: freynaud
'''
from subprocess import CalledProcessError
import http.server
import json
import socketserver
import subprocess
import urllib.parse
    
    
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
        print("START POST CALL")
        length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(length)
        
        if (post_data):
            json_content = post_data.decode("UTF-8")
            j = json.loads(json_content)
            print(json.dumps(j, sort_keys=True, indent=4))
            command = j['cmd']
            if (not command):
                res = {"success":False,"content":"valid command contain a cmd key \"cmd\"."}
            else :
                try:
                    print("will execute : ")
                    print(command)
                    b = subprocess.check_output(command,stderr=subprocess.STDOUT)
                    print(b)
                    res = {"success":True,"content":b.decode("UTF-8")}
                except OSError as err:
                    res = {"success": False,"content":err.strerror}
                except CalledProcessError as err :
                    o = err.output
                    res = {"success": False, "returncode":err.returncode, "content":o.decode("UTF-8")}
        else:
            res = {"success": False,"content":"post has no content."}
        
        self.send_response(200, "success")
        self.end_headers()
        content = json.dumps(res)
        b = bytes(content, "UTF-8")
        self.wfile.write(b)
        print("END POST CALL")
     


if __name__ == '__main__':
    print("Starting command center on port 5558")
    PORT = 5558
    Handler = MyHandler
    try :
        httpd = socketserver.TCPServer(('', PORT), Handler)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("stopping")
        httpd.socket.close()
