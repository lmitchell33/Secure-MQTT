import paho.mqtt.client as mqtt
import os
import ssl
from time import sleep
from datetime import datetime
import logging


class MQTTPublisher:
    def __init__(self, broker:str, port:int, topic:str, username:str, password:str):
        '''Constructor for the MQTT subscriber class
        Args:
            broker {int} -- IP address for the broker/proxy to connect to
            port {int} -- port to run the subscriber process on

        Kwargs:
            topics {str} -- topic the subscriber should initally subscribe to

        Returns:
            None
        '''
        
        if broker is None or type(broker) != str:
            raise TypeError("Broker argument is required and must be an string")
        if port is None or type(port) != int:
            raise TypeError("Port argument is required and must be an integer")
        if topic is None or type(topic) != str:
            raise TypeError("Topic argument is required and must be an integer")
        
        self.broker = broker
        self.port = port
        self.topic = topic
        self.username = username
        self.password = password

        base_dir = os.path.expanduser("~/SSL-IoT/Broker/config")

        # create a client object (id=1) with the specified certificates
        self.client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id="publisher 2")
        self.client.tls_set(
            ca_certs=f'{base_dir}/certs/ca.crt',
            certfile=f'certs/publisher.crt',
            keyfile=f'certs/publisher.key',
            cert_reqs=ssl.CERT_REQUIRED, 
            tls_version=ssl.PROTOCOL_TLSv1_2
        )

        self.client.tls_insecure_set(True)

        # set the callback functions of the client object to the functions we created below
        self.client.on_connect = self.on_connect
        # self.client.on_publish = self._on_publish
        
        # TODO: uncomment this when authentication is setup
        self.client.username_pw_set(username=self.username, password=self.password)

        # NOTE: maybe want to change the keepalive to longer
        self.client.connect(self.broker, self.port, 60)

    
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

        if (reason_code == 0):
            print(f"Successfully connected with result code {reason_code}")
        else:
            print(f"Connection failed with result code {reason_code}")

    
    # def _on_publish(self, client, userdata, mid):
    #     """Publish callback"""
    #     print(f"Message {mid} pubslihed")
    #     # self.logger.info(f"Message {mid} published successfully")

    
    def start(self):
        self.client.loop_start()


    def publish(self, message=None, qos=1, retain=False):
        result = self.client.publish(self.topic, payload=message, qos=qos, retain=retain)
        result.wait_for_publish()



if __name__ == "__main__":
    topic = "test/sensor"
    laptop_IP = "192.168.68.53"
    username = "test_publisher"
    password = "mightyhippo917"
    port = 8883


    publisher = MQTTPublisher(broker=laptop_IP, port=port, topic=topic, username=username, password=password)
    publisher.start()

    while True:
        publisher.publish(message="Hello World")
        sleep(2)
    