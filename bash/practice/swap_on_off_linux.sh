#!/usr/bin/env bash

# Author - Vijay Anand.P
# Credits - Justin.B
# Date - 01/02/2016
# This script is to add the new swap space in the linux for increasing the system speed or 
# to avoid the program crashes
# Note: Run as a ROOT, it supports only Linux

ss="\n******************************************************************** "
sudo swapoff /new_swap

function disk_usage() {
echo "Current Disk Space"
free -mh
echo -e "\n\n"
df -h 
echo -e $ss
}

disk_usage

sudo  dd if=/dev/zero of=/new_swap bs=100M count=2  # Create a 200MB disk block under '/'

sudo mkswap /new_swap

sudo swapon /new_swap

echo -e $ss

disk_usage

# swapoff /new_swap

# dd if=/dev/zero of=/new_swap count=1 bs=100M
# df -h
# du -d 1 -h
# mkswap
# swapon
# swapoff
# free -mh