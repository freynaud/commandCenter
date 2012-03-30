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
    

version = "1235"


class JsonRequest:
    
    _raw = None
    _json = None
    _async = False
    command = None
    
    def __init__(self, raw_request):
        print(raw_request)
        self._raw = raw_request
        self._json = json.loads(raw_request)
        self._async = (self._json['async'] == True)
        self.command = self._json['cmd']
    
    
    def is_asyncronous(self):
        return self._async
    
    
    def dumps(self):
        return self._raw
    
class JsonResponse:
    
    success = False
    returnCode = 0
    content = None
    _request = None
    
    """
        request is a JSONRequest
    """
    def __init__(self, success=True, returnCode=0, content=None, request=None):
        self.success = success
        self.returnCode = returnCode
        self.content = content
        self._request = request
    
    """
    return the json string for the request 
    """
    def dumps(self):
        res = {"success":self.success, "content": self.content , "request" : self._request.dumps(), "returnCode" : self.returnCode}
        json_string = json.dumps(res)
        return json_string

class Executor:
    
    _json_request = None
    
    def __init__(self, json_request):
        self._json_request = json_request
        
    def execute(self):
        res =JsonResponse(request=self._json_request)
        try:
            if self._json_request.is_asyncronous() :
                subprocess.Popen(self._json_request.command)
                res.content = "N/A , async call - no output"
            else :
                b = subprocess.check_output(self._json_request.command,stderr=subprocess.STDOUT)
                res.content = b.decode("UTF-8")
        except OSError as err:
            res.success = False
            res.content =err.strerror
        except CalledProcessError as err :
            res.success = False
            o = err.output
            res.returnCode=err.returncode
            res.content=o.decode("UTF-8")
        except ValueError as err:
            res.success = False
            res.content="value error ( wrong input )"
        return res

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print(self)
       
        res = urllib.parse.urlparse(self.path)
        query = res[4];
        params = urllib.parse.parse_qs(query)
        j = params['json']
        b = bytes("<html><body>" + version + "</body></html>\n", "UTF-8"); 
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
        post_data = self.rfile.read(length)
        
        if (post_data):
            raw_json_content = post_data.decode("UTF-8")
            request =  JsonRequest(raw_json_content)
            
            exe = Executor(request);
            json_response = exe.execute()
        else:
            json_response =JsonResponse(content="post has no content.")
        self.send_response(200, "success")
        self.end_headers()
        content = json_response.dumps()
        b = bytes(content, "UTF-8")
        self.wfile.write(b)
     


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
