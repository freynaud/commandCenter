'''
Created on 10 Mar 2012

@author: freynaud
'''

import LinuxNetworkInterface
import time

def no_op():
    print("no op")

def wait_for_ip():
    interface = LinuxNetworkInterface.LinuxNetworkInterface("00:0c:29:cd:ad:02")
    interface.mark_up = no_op
    if (not interface.is_up()):
        interface.mark_up()
    
    while True:
        ip = interface.get_ip_v4()
        if (ip):
            return ip
        else :
            time.sleep(1)

if __name__ == '__main__':
    os = "LINUX"
    
    if (os == "LINUX"):
        ip = wait_for_ip()
        print("ip:"+ip)
    else :
        pass