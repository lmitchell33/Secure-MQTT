# **Secure Implementation of the MQTT Protocol**

## **Overview**

This project implements a fully secure MQTT-based communication system for IoT devices. It provides a reliable and encrypted channel for message exchange between publishers and subscribers through an MQTT broker. The system leverages a reverse proxy (NGINX) for enhanced security and scalability, ensuring robust protection for IoT data. The MQTT broker also utilizes a logging feature to log any abnormalities, allowing for quicker detection of any threats.

## **Technical Stack**

- **MQTT Broker:** Mosquitto
- **Reverse Proxy:** NGINX
- **Containerization:** Docker
- **Encryption:** TLS (Transport Layer Security)
- **Programming Languages:** Python, Bash

## **Getting Started**

Follow the steps below to set up and use the secure MQTT system. You may use other subscribers and publishers as long as you update the ACL with their username and password.

### **1. Clone the Repository**

`git clone https://github.com/lmitchell33/Secure-MQTT.git && cd Secure-MQTT`

### **2. Generate Certificates**

Since self-signed certificates are being used, you must generate your own Certificate Authority (CA) and the certificates for each component in the system. The `generate-certs.sh` script automates this process by creating a certificate and key for each component.

- The certificates and keys for the publisher and subscriber will be placed in the `/certs` subdirectory.
- The CA and the broker's certificates will be placed in the `/config/certs` subdirectory within the Broker directory.

**Note**: Ensure the ca.ext file is updated with your system's IP address(es) under the [alt_names] section.

`chmod +x Scripts/generate-certs.sh && ./generate-certs.sh`

### **3. Optional: Install the Python Requirements**

The only Python dependency for this demonstration is the paho-mqtt library, used by the publisher and subscriber.

**Note**: This step can be skipped if external devices are used as publishers and subscribers.

`pip install -r requirements.txt`

### **4. Build the Docker Compose**

Navigate to the Broker directory and build the Docker containers for the proxy and broker servers:

`cd Broker`

`docker compose build`

### **5. Start the Docker Containers**

Start the proxy and broker servers:

`docker compose up`

### **6. Start the Subscriber**

Run the subscriber to listen on the test/topic topic.

**Note**: Update the IP address, port, and topic in the script as needed:

`cd ..`

`python3 Subscriber/mqtt_subscriber.py`

### **7. Start the Publisher**

Run the publisher to send data to the test/topic topic.

**Note**: Update the IP address, port, and topic in the script as needed:

`python3 Publisher/mqtt_publisher.py`

## **Collaborators**

- Lucas Mitchell
