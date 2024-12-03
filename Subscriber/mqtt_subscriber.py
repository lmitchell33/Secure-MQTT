import paho.mqtt.client as mqtt
import os
import ssl

# NOTE: the paho-mqtt library is made by the same developers/company as mosquitto
# which is why I chose it

USERNAME = "testuser1"
PASSWORD = "Soccer0104*23"

class MQTTSubscriber:
    def __init__(self, broker:str, port:int, topic:str):
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
        
        self.topic = topic

        base_dir = os.path.expanduser("~/SSL-IoT/Broker/config")

        # create a client object (id=1) with the specified certificates
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="1")
        self.client.tls_set(
            ca_certs=f'{base_dir}/certs/ca.crt',
            certfile=f'certs/subscriber.crt',
            keyfile=f'certs/subscriber.key',
            cert_reqs=ssl.CERT_REQUIRED, 
            tls_version=ssl.PROTOCOL_TLSv1_2
        )

        self.client.tls_insecure_set(True)

        # set the callback functions of the client object to the functions we created below
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        # TODO: uncomment this when authentication is setup
        self.client.username_pw_set(username=USERNAME, password=PASSWORD)

        # NOTE: maybe want to change the keepalive to longer
        self.client.connect(broker, port, 60)


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

        client.subscribe(self.topic)


    def on_message(self, client, userdata, msg):
        ''' Message callback function to be called by the Client object to display the message received
        Args:
            client {obj} -- Paho-MQTT client object for the callback
            userdata {obj} -- user data given to the callback function by the client
            msg {obj} -- msg given to the client obj about the topic
        Kwargs:
            None
        Returns:
            None
        '''
        print(f"Received: {msg.topic} {msg.payload}")


    def start(self):
        '''Function to start the Client object
        Args: 
            None
        Kwargs:
            None
        Returns:
            None
        '''
        # Because this program only wants to run one client, we can loop forever
        # otherwise, we would have to manually start and stop the loop
        self.client.loop_forever()


if __name__ == "__main__":
    topic = "test/sensor"
    laptop_IP = "192.168.68.53"
    subscriber = MQTTSubscriber(broker=laptop_IP, port=443, topic=topic)
    subscriber.start()