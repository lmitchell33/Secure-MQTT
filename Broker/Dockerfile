FROM ubuntu:latest

# Ensure apt-get is available and install iptables
RUN apt-get update && apt-get install -y iptables && apt-get clean

# Copy your script into the container
COPY ./firewall.sh /bin/firewall.sh

# Ensure the script is executable
RUN chmod +x /bin/firewall.sh

# Set the entrypoint
ENTRYPOINT ["/bin/bash", "/bin/firewall.sh"]