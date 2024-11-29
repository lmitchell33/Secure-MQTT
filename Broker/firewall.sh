#!/bin/bash

set -e

iptables -F # flush the existing iptables
iptables -X # Delete  the optional user-defined chain (optional)
iptables -Z # zero the byte and pakcet counters in all chains

iptables -P INPUT DROP
iptables -P OUTPUT ACCEPT
iptables -P FORWARD DROP

# allow a loopback interface
iptables -A INPUT -i lo -j ACCEPT

# Allow SSH
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Allow established and related connections
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Allow traffic to NGINX HTTPS (Port 443) only from trusted IPs
iptables -A INPUT -p tcp --dport 443 -s 192.168.1.0/24 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -s 203.0.113.0/24 -j ACCEPT

# Allow local traffic to the Mosquitto broker (NGINX proxy needs this)
iptables -A INPUT -p tcp --dport 8883 -s 127.0.0.1 -j ACCEPT

# Drop other incoming traffic on these ports
iptables -A INPUT -p tcp --dport 443 -j DROP
iptables -A INPUT -p tcp --dport 8883 -j DROP