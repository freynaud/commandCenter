
from SnapshortRevertedListener import SnapshotListener
from subprocess import CalledProcessError
import glob
import subprocess
import sys
import LinuxNetworkInterface
import time


def _get_mac_address():
    return sys.argv[1]


def refresh_network():
    print("refresh network")
    try :
        output = subprocess.check_output(["sudo", "/sbin/dhclient","-r" ])
        files = glob.glob("/var/lib/dhcp3/*")
        for file in files :
            output = subprocess.check_output(["sudo", "rm",file ])
        interface = LinuxNetworkInterface.LinuxNetworkInterface(_get_mac_address())
        output = subprocess.check_output(["sudo", "/sbin/dhclient",interface._get_interface() ])
    except CalledProcessError as ex:
        return output.decode("UTF-8")
    print("network refreshed")

def update_itself():
    print("updating itself.")
    ok = False
    while  not ok :
        try:
            b = subprocess.check_output(["git","pull","origin","master"])
            ok = True
            print(b.decode("UTF-8"))
        except Exception as err:
            print(err)
    


def send_ready_signal():
    print("about to send rdy signal")
    try:
        b = subprocess.check_output(["python3.2","sendReadySignal.py",_get_mac_address()])
    except CalledProcessError as ex:
        print(ex.output)
    print("signal sent")

def start_command_center():
    print("start_command_center")
    try:
        b = subprocess.check_output(["python3.2","startCommandCenterServer.py"],stderr=subprocess.STDOUT)
    except CalledProcessError as ex:
        print(ex.output)



def launch():
    refresh_network()
    update_itself()
    #send_ready_signal()
    start_command_center()



if __name__ == '__main__':
    #listener = SnapshotListener(callback=launch)
    #listener.start()
    launch()
    