import socketserver
import CommandCenter

if __name__ == '__main__':
    
  PORT = 8081
  Handler = CommandCenter.MyHandler
  httpd = socketserver.TCPServer(('', PORT), Handler)
  httpd.serve_forever()