#!/bin/bash

# NOTE: This firewall should be set on the host machine

# exit on error
set -e

# flush tables and delete user-defined chains in current rules 
iptables -F 
iptables -X 

# by default, deny 
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Allow loopback (localhost on 127.0.0.1) traffic
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Allow established and related connections and prevent interrupting ongoing connections
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT


# Method 1: Allow all incoming traffic to proxy 
# Allow incoming traffic to NGINX (port 443)
# iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Method 2: 
# only accept incoming connections from my hotspots IP on port 443 and drop everything else
iptables -A INPUT -p tcp -s 174.242.0.0/16 --dport 443 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j DROP


# Log and drop all other incoming traffic
iptables -A INPUT -j LOG --log-prefix "IPTables-Dropped: " --log-level 4
iptables -A INPUT -j DROP
