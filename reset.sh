#!/bin/bash
sudo ifconfig eth0 down
sudo dhclient -r 
sudo rm -f /var/lib/dhcp/*