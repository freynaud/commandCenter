'''
Created on 14 Mar 2012

@author: freynaud
'''

import json
import LinuxNetworkInterface
import http.client
import sys

def get_mac_address():
    return sys.argv[1]

def send_ready_signal():
    print("about to send rdy signal")
    mac = get_mac_address()
    interface = LinuxNetworkInterface.LinuxNetworkInterface(mac)
    body = json.dumps({"cmd":"NodeWokeUpEvent", "content" :{"mac":mac , "ip":interface.get_ip_v4()}})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = http.client.HTTPConnection("10.250.57.219:4444",timeout=10)
    conn.request("POST", "/grid/admin/NodeCommandCenterServlet/", body, headers)
    response = conn.getresponse()
    print(response.status, response.reason)
    data = response.read()
    print(data)
    conn.close()
    
if __name__ == '__main__':
    send_ready_signal()