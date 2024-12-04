#!/bin/bash

set -e

apt-get update && apt-get install -y iptables

# flush tables and delete user-defined chains in current rules 
iptables -F 
iptables -X 
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X

# by default, drop all incoming traffic
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Allow loopback traffic
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Allow established and related connections and prevent interrupting ongoing connections
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Allow incoming traffic to NGINX (port 443)
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# # Allow internal Docker network communication (mosquitto_network)
# DOCKER_NETWORK="172.18.0.0/16"  # Replace with your Docker bridge network CIDR if different
# iptables -A INPUT -s $DOCKER_NETWORK -j ACCEPT

# # Allow Mosquito broker traffic on port 8883 from NGINX
# iptables -A INPUT -p tcp --dport 8883 -s $DOCKER_NETWORK -j ACCEPT

# Allow Mosquitto broker traffic on 127.0.0.1:8883
iptables -A INPUT -p tcp --dport 8883 -i lo -j ACCEPT

# Log and drop all other incoming traffic
iptables -A INPUT -j LOG --log-prefix "IPTables-Dropped: " --log-level 4
iptables -A INPUT -j DROP

# Save iptables rules to ensure persistence
# iptables-save > /etc/iptables/rules.v4