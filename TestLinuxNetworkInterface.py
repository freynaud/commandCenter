'''
Created on 10 Mar 2012

@author: freynaud
'''
import unittest
import LinuxNetworkInterface

class Mock(LinuxNetworkInterface.LinuxNetworkInterface):
   
    eth0_hwaddr = "00:0c:29:cd:ad:02"
    eth1_hwaddr = "00:0c:29:cd:ad:03"
   
    
    eth0_first_line = "eth0      Link encap:Ethernet  HWaddr 00:0c:29:cd:ad:02  "
    eth1_first_line = "eth1      Link encap:Ethernet  HWaddr 00:0c:29:cd:ad:03  "
   
    eth0_ip = "192.168.157.129"
    ifconfig_eth0 = "\
eth0      Link encap:Ethernet  HWaddr 00:0c:29:cd:ad:02  \n\
          inet addr:192.168.157.129  Bcast:192.168.157.255  Mask:255.255.255.0\n\
          inet6 addr: fe80::20c:29ff:fecd:ad02/64 Scope:Link\n\
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1\n\
          RX packets:11133 errors:0 dropped:0 overruns:0 frame:0\n\
          TX packets:7894 errors:0 dropped:0 overruns:0 carrier:0\n\
          collisions:0 txqueuelen:1000 \n\
          RX bytes:13564944 (13.5 MB)  TX bytes:672472 (672.4 KB)\n\
          Interrupt:19 Base address:0x2024 \n\
\n"
    ifconfig_eth1 = "\
eth1      Link encap:Ethernet  HWaddr 00:0c:29:cd:ad:03  \n\
          BROADCAST MULTICAST  MTU:1500  Metric:1\n\
          RX packets:11419 errors:0 dropped:0 overruns:0 frame:0\n\
          TX packets:8173 errors:0 dropped:0 overruns:0 carrier:0\n\
          collisions:0 txqueuelen:1000 \n\
          RX bytes:13716679 (13.7 MB)  TX bytes:709711 (709.7 KB)\n\
          Interrupt:19 Base address:0x2024\n\
\n"

    ifconfig_lo = "\
lo        Link encap:Local Loopback  \n\
          inet addr:127.0.0.1  Mask:255.0.0.0\n\
          inet6 addr: ::1/128 Scope:Host\n\
          UP LOOPBACK RUNNING  MTU:16436  Metric:1\n\
          RX packets:7373 errors:0 dropped:0 overruns:0 frame:0\n\
          TX packets:7373 errors:0 dropped:0 overruns:0 carrier:0\n\
          collisions:0 txqueuelen:0 \n\
          RX bytes:1775131 (1.7 MB)  TX bytes:1775131 (1.7 MB)\n"  
          
    ifconfig_a = ifconfig_eth0 + ifconfig_eth1 + ifconfig_lo
    
    def __init__(self, hwaddr, ifconfig=ifconfig_a):
        '''
        Constructor. set the result of a 
        ifconfig -a call for testing purposes.
        '''
        self.ifconfig_result = ifconfig
        self._hwaddr = hwaddr
        
    def _execute_ifconfig(self, interface_name="-a"):
        if ("-a" == interface_name):
            return self.ifconfig_a
        elif ("eth0" == interface_name):
            return self.ifconfig_eth0
        elif ("eth1" == interface_name):
            return self.ifconfig_eth1
        elif ("lo" == interface_name):
            return self.ifconfig_lo
        else :
            return None
    
    

class Test(unittest.TestCase):
    
           
    def test_extract_interface(self):
        interface = LinuxNetworkInterface.LinuxNetworkInterface(None)
        self.assertEqual(interface._get_interface_name_for_line(Mock.eth0_first_line), "eth0")
        self.assertEqual(interface._get_interface_name_for_line(Mock.eth1_first_line), "eth1")
        
    def test_get_all_interfaces(self):
        interface = Mock(Mock.eth0_hwaddr)
        interfaces = interface._get_all_interfaces();
        self.assertEqual(len(interfaces), 2)
        self.assertIn("eth0", interfaces)
        self.assertIn("eth1", interfaces)
        
    def test_get_interface_for_mac_address(self):
        interface = Mock(Mock.eth0_hwaddr)
        self.assertEqual(interface._get_interface(), "eth0")
        
        interface = Mock(Mock.eth1_hwaddr)
        self.assertEqual(interface._get_interface(), "eth1")
        
    def test_exist(self):
        interface = Mock(Mock.eth0_hwaddr)
        self.assertTrue(interface.exists())
        
        interface = Mock(Mock.eth1_hwaddr)
        self.assertTrue(interface.exists())
        
        interface = Mock("00:0c:29:cd:ad:00")
        self.assertFalse(interface.exists())
        
    def test_is_up(self):
        interface = Mock(Mock.eth0_hwaddr)
        self.assertTrue(interface.is_up())
        
        interface = Mock(Mock.eth1_hwaddr)
        self.assertFalse(interface.is_up())
    
    def test_get_ip(self):
        interface = Mock(Mock.eth0_hwaddr)
        self.assertEqual(interface.get_ip_v4(),Mock.eth0_ip)
        
        interface = Mock(Mock.eth1_hwaddr)
        self.assertEqual(interface.get_ip_v4(),None)
         

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    


