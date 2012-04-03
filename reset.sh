#!/bin/bash
ifconfig eth0 down
dhclient -r 
rm /var/lib/dhcp/*