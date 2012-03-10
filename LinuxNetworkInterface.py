'''
Created on 10 Mar 2012

@author: freynaud
'''
import subprocess

class LinuxNetworkInterface:
    '''
    wrapper around ifconfig.
    '''

    _hwaddr = None

    def __init__(self, hwaddr):
        '''
        Constructor
        '''
        self._hwaddr = hwaddr
    
    def _execute_ifconfig(self , interface_name ="-a"):
        output = subprocess.check_output(["ifconfig", interface_name])
        return output.decode("UTF-8")
    
   
    
    def _get_interface_name_for_line(self, interface_desc_first_line):
        """
        extract the interface name ( eth0 , lo ) from the interface description 
        """
        
        start = 0
        end = interface_desc_first_line.find("      Link encap")
        res = interface_desc_first_line[start:end]
        return res
    
    def _get_interface_first_linel(self, ifconfig_a_result):
        """
        get all network interfaces. Ignores lo
        """
        res = []
        lines = ifconfig_a_result.splitlines()
        for line in lines :
            if ("HWaddr" in line) :
                res.append(line)
        return res  
    
    def _get_all_interfaces(self):
        res = []
        ifconfig = self._execute_ifconfig()
        first_lines = self._get_interface_first_linel(ifconfig)
        for line in first_lines:
            res.append(self._get_interface_name_for_line(line))
        return res
    
   
    
    def _get_interface(self):
        """ 
        get the interface associated to the hwaddr that was 
        provided while creating that NetworkInterface object.
        """
        ifconfig = self._execute_ifconfig()
        first_lines = self._get_interface_first_linel(ifconfig)
        for line in first_lines:
            if ( self._hwaddr in line ):
                return self._get_interface_name_for_line(line)
        return None
    
    def exists(self):
        ifconfig = self._execute_ifconfig()
        first_lines = self._get_interface_first_linel(ifconfig)
        for line in first_lines:
            if ( self._hwaddr in line ):
                return True
        return False
    
    def is_up(self):
        res = self._execute_ifconfig(self._get_interface())
        return "inet" in res
    
    def get_ip_v4(self):
        res = self._execute_ifconfig(self._get_interface())
        lines = res.splitlines()
        prefix = "inet addr:"
        for line in lines:
            if (prefix in line):
                start = line.index(prefix) + len(prefix)
                end = line.find(" ", start)
                ip = line[start:end]
                return ip
        return None

if __name__ == '__main__':
    interface = LinuxNetworkInterface("00:0c:29:cd:ad:02")
    print(interface.get_ip_v4())
    
