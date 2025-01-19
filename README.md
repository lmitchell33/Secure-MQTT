# **Secure Implementation of the MQTT Protocol**

## **Overview**

This project was created as my final project for COSC 460: Computer Security. It implements a fully secure MQTT-based communication system for IoT devices. It provides an encrypted channel for message exchange between clients through an MQTT broker. The system leverages a reverse proxy (NGINX) for enhanced security and scalability, ensuring robust protection for IoT data.

## **Built With**

- **MQTT Broker:** Mosquitto
- **Reverse Proxy:** NGINX
- **Containerization:** Docker
- **Encryption:** TLS (Transport Layer Security)
- **Programming Languages:** Python, Bash
- **Operating System:** Unix/Linux (Ubuntu)

## **Getting Started**

Follow the steps below to set up and use the secure MQTT system. You may use other clients, however, you must update the ACL with their username/password, see mosquitto documentation for this.

### Installation

1. Clone the repository

```sh
git clone https://github.com/lmitchell33/Secure-MQTT.git && cd Secure-MQTT
```

2. Optional: Generate Certificates

Since self-signed certificates are being used, you must generate your own Certificate Authority (CA) and the certificates for each component in the system. The `generate-certs.sh` script automates this process by creating a certificate and key for each component.

- The certificates and keys for the publisher and subscriber will be placed in the `/certs` subdirectory.
- The CA and the broker's certificates will be placed in the `/config/certs` subdirectory within the Broker directory.

**Note**: Ensure the ca.ext file is updated with your system's IP address(es) under the [alt_names] section.

```sh
chmod +x Scripts/generate-certs.sh && ./generate-certs.sh
```

3. Install Python libraries

```sh
pip install -r requirements.txt
```

3. Build the Docker compose

```sh
cd Broker
docker compose build
```

## **Usage**

1. Start the Docker Containers

```sh
docker compose up
```

2. Update the Broker's IP address and port

```sh
export PUBLIC_IP="your ip address"
export EXTERNAL_PORT="your port number"
```

Note: The next steps depend on what clients you use. Using the tests clients found in this repo, you must do the following:

3. Start the subscriber

```sh
cd ..
python3 Subscriber/mqtt_subscriber.py
```

3. Start the publisher

```sh
python3 Publisher/mqtt_publisher.py
```

## **Collaborators**

- Lucas Mitchell
