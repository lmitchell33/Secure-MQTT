import paho.mqtt.client as mqtt
import os
import ssl
from time import sleep
import logging
from datetime import datetime


class MQTTPublisher:
    def __init__(self, broker, port, topic, username, password):
        '''Constructor for the MQTT subscriber class
        Args:
            broker {int} -- IP address for the broker/proxy to connect to
            port {int} -- port to run the subscriber process on

        Kwargs:
            topics {str} -- topic the subscriber should initally subscribe to

        Returns:
            None
        '''
        
        if not isinstance(broker, str):
            raise TypeError("Broker argument is required and must be an string")
        if not isinstance(broker, str):
            raise TypeError("Port argument is required and must be an integer")
        if not isinstance(broker, str):
            raise TypeError("Topic argument is required and must be an integer")
        if not isinstance(username, str):
            raise TypeError("Password argument is required and must be an string")
        if not isinstance(password, str):
            raise TypeError("Username argument is required and must be an string")

        # create and setup a logger 
        self.logger = logging.getLogger("MQTTPublisher")
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler("mqtt_publisher.log")
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(handler)
        
        self.broker = broker
        self.port = port
        self.topic = topic
        self.username = username
        self.password = password

        base_dir = os.path.expanduser("~/SSL-IoT/Broker/config")

        try:
            # create a client object specifying the callback version and a unique id
            self.client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id="publisher_1")
            self.client.tls_set(
                ca_certs=f'{base_dir}/certs/ca.crt',
                certfile=f'certs/publisher.crt',
                keyfile=f'certs/publisher.key',
                cert_reqs=ssl.CERT_REQUIRED, 
                tls_version=ssl.PROTOCOL_TLSv1_2
            )
        except Exception as e:
            self.logger.exception("Failed to setup TLS config")
            raise e

        self.client.tls_insecure_set(False)

        # set the callback functions of the client object to the functions we created below
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        
        try:
            # set the username and password combo
            self.client.username_pw_set(username=self.username, password=self.password)
        except Exception as e:
            self.logger.exception("Failed to establish username and password with broker")
            raise e

        try:
            # connect to the broker
            self.client.connect(self.broker, self.port, 60)
            self.logger.info("Client successfully connected to broker")
        except Exception as e:
            self.logger.exception("Failed to connect to broker")
            raise e

    
    def on_connect(self, client, userdata, flags, reason_code, properties):
        ''' Connect callback function to be called by the Client object when connecting to a broker
        Args:
            client {obj} -- Paho-MQTT client object for the callback
            userdata {obj} -- user data given to the callback function by the client
            flags {obj} -- flags given to the callback function by the client
            reason_code {int} -- similar to an HTTP status code
            properties {obj} -- properties of the client
        Kwargs:
            None
        Returns:
            None
        '''

        # check if the connection was successful and log the success or failure
        if reason_code == 0:
            self.logger.info(
                f"Successfully connected to broker at {self.broker}:{self.port}. "
                f"Client ID: {client._client_id.decode('utf-8')}, Topic: {self.topic}"
            )
        else:
            self.logger.error(
                f"Connection to broker at {self.broker}:{self.port} failed. Reason Code: {reason_code}. "
                f"Flags: {flags}. Potential issue with credentials or network."
            )

    
    def on_publish(self, client, userdata, message_id, reason_code=None, properties=None):
        """Publish callback"""
        # check if a message was successfully published and log the success or failure
        if reason_code == 0:
            self.logger.info(
                f"Successfully published to topic '{self.topic}' on broker {self.broker}:{self.port}. "
                f"Message ID: {message_id}"
            )        
        else:
            self.logger.error(
                f"Failed to publish to topic '{self.topic}' on broker {self.broker}:{self.port}. ")

    
    def start(self):
        '''Start the MQTT publisher process'''
        try:
            # attempt to start the client and log the success
            self.logger.info(
                f"Starting MQTT publisher on broker {self.broker}:{self.port},"
                f"Client ID: {self.client._client_id.decode('utf-8')}, Topic: {self.topic}"
            )
            self.client.loop_start()
        
        # Log common errors
        except KeyboardInterrupt:
            self.logger.info("MQTT publisher stopped by user")
        except Exception as e:
            self.logger.exception("{e} error occured while the subscriber was running.")


    def publish(self, message=None, qos=1, retain=False):
        '''Publish a message to the broker'''
        try:
            # attempt to publish and log the success
            result = self.client.publish(self.topic, payload=message, qos=qos, retain=retain)
            result.wait_for_publish()
            self.logger.info(f"Publish request sent for topic '{self.topic}' to broker {self.broker}:{self.port}.")
        except Exception as e:
            self.logger.exception(f"Failed to send publish request for topic '{self.topic}'. Error: {e}")


if __name__ == "__main__":
    topic = "test/sensor"
    
    # IPs testing with
    internal_IP = os.getenv("INTERNAL_IP")
    public_IP = os.getenv("PUBLIC_IP")    
    school_IP = os.getenv("SCHOOL_IP")    

    username = os.getenv("GOOD_PUB_USERNAME") 
    password = os.getenv("GOOD_PUB_PASSWORD") 

    # bad credentials
    # username = "Test" 
    # password = "Test"

    internal_port = int(os.getenv("INTERNAL_PORT")) 
    external_port = int(os.getenv("EXTERNAL_PORT")) 


    # publisher = MQTTPublisher(broker=public_IP, port=external_port, topic=topic, username=username, password=password)
    publisher = MQTTPublisher(broker=internal_IP, port=internal_port, topic=topic, username=username, password=password)
    # publisher = MQTTPublisher(broker=school_IP, port=internal_port, topic=topic, username=username, password=password)

    publisher.start()

    while True:    
        publisher.publish(f"Hello World sent at: {datetime.now()}")
        sleep(2)
    