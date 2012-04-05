#!/bin/bash
sudo mount -t smbfs //10.250.57.200/share /home/euqe/share
sudo ifconfig eth0 down
sudo dhclient -r 
sudo rm -f /var/lib/dhcp/*
