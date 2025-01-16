#!/bin/bash

# NOTE: This firewall should be set on the host machine

# flush tables and delete user-defined chains in current rules 
iptables -F 

# Default deny
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Allow localhost traffic needed for the docker network
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Allow established and related connections and prevent interrupting ongoing connections
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# only accept incoming connections from my hotspots IP on port 443 and drop everything else
iptables -A INPUT -p tcp -s 192.168.0.0/16 --dport 443 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j DROP

# Drop all other incoming traffic
iptables -A INPUT -j DROP

