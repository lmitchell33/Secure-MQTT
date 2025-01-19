import paho.mqtt.client as mqtt
import os
import ssl
import logging
from datetime import datetime

# NOTE: the paho-mqtt library is made by the same developers/company as mosquitto
# which is why I chose it


class MQTTSubscriber:
    def __init__(self, broker, port, topic, username, password):
        '''Constructor for the MQTT subscriber class
        Args:
            broker {int} -- IP address for the broker/proxy to connect to
            port {int} -- port to run the subscriber process on
            topic {str} -- topic the subscriber should initally subscribe to
            username {str} -- username for the broker
            password {str} -- password for the broker
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
        self.logger = logging.getLogger("MQTTSubscriber")
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler("mqtt_subscriber.log")
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(handler)

        self.topic = topic
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password
        self.time_diffs = []

        base_dir = os.path.expanduser("~/SSL-IoT/Broker/config")

        try:
            # create a client object specifying the callback version and a unique id
            self.client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id="subscriber_1")
            self.client.tls_set(
                ca_certs=f'{base_dir}/certs/ca.crt',
                certfile=f'certs/subscriber.crt',
                keyfile=f'certs/subscriber.key',
                cert_reqs=ssl.CERT_REQUIRED, 
                tls_version=ssl.PROTOCOL_TLSv1_2
            )
        except Exception as e:
            self.logger.exception("Failed to setup TLS config")
            raise e

        self.client.tls_insecure_set(False)

        # set the callback functions of the client object to the functions we created below
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_subscribe = self.on_subscribe
        
        try:
            self.client.username_pw_set(username=self.username, password=self.password)
        except Exception as e:
            self.logger.exception("Failed to establish username and password with broker")
            raise e

        try:
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

        self.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        ''' Message callback function to be called by the Client object to display the message received
        Args:
            client {obj} -- Paho-MQTT client object for the callback
            userdata {obj} -- user data given to the callback function by the client (typically none)
            msg {obj} -- msg given to the client obj about the topic
        Kwargs:
            None
        Returns:
            None
        '''
        message = msg.payload.decode('utf-8')

        if len(message) > 4096: 
            # do not let in messages over a the maximum allowed by the broker, delete the message and log an error
            self.logger.error(f"Size of message received from topic: '{self.topic}' is over the limit set by the broker. Size: {len(message)} bytes")
            del message
            return

        self.logger.info(f"Message received on topic: '{msg.topic}' from broker {self.broker}:{self.port} and publisher. Size: {len(message)} bytes")

        time = datetime.strptime(str(str(message).split("sent at: ")[1]), "%Y-%m-%d %H:%M:%S.%f")
        curr_time_diff = (datetime.now() - time).total_seconds()

        # NOTE: this print statement would typically either be a display for a UI or some sort of processing
        print(f"Received: {message}, time diff: {curr_time_diff}")
        self.time_diffs.append(curr_time_diff)

        if len(self.time_diffs) == 100:
            print("The average time difference for the encrypted communication was: ", sum(self.time_diffs)/len(self.time_diffs))
            self.client.loop_stop()


    def on_subscribe(self, client, usedata, message_id, granted_qos, properties=None):
        '''Subscribe callback function to be called by the Client object when subscribing to a topic'''
        # check if the subscription was successful and log the success or failure
        if granted_qos[0] == 0:
            self.logger.info(
                f"Successfully subscribed to topic '{self.topic}' on broker {self.broker}:{self.port}. "
                f"Granted QoS: {granted_qos}. Message ID: {message_id}"
            )
        else:
            self.logger.error(
                f"Failed to subscribe to topic '{self.topic}' on broker {self.broker}:{self.port}. ")


    def subscribe(self, topic):
        '''Subscribe to a topic on the broker'''
        try:
            # attempt to subscribe to the topic and log the success
            self.client.subscribe(topic)
            self.logger.info(f"Subscription request sent for topic '{topic}' to broker {self.broker}:{self.port}.")
        except Exception as e:
            self.logger.exception(f"Failed to send subscription request for topic '{topic}'. Error: {e}")


    def start(self):
        '''Function to start the Client object'''
        # Because this program only wants to run one client, we can loop forever
        # otherwise, we would have to manually start and stop the loop
        try:
            self.logger.info(
                f"Starting MQTT subscriber on broker {self.broker}:{self.port},"
                f"Client ID: {self.client._client_id.decode('utf-8')}, Topic: {self.topic}"
            )
            self.client.loop_forever()
        except KeyboardInterrupt:
            self.logger.info("MQTT subscriber stopped by user")
        except Exception as e:
            self.logger.exception("{e} error occured while the subscriber was running.")


if __name__ == "__main__":
    topic = "test/sensor"
    
    # IPs testing with
    # internal_IP = os.getenv("INTERNAL_IP")
    public_IP = os.getenv("PUBLIC_IP") # public ip address for the broker
    # school_IP = os.getenv("SCHOOL_IP")    

    username = os.getenv("GOOD_SUB_USERNAME") 
    password = os.getenv("GOOD_SUB_PASSWORD") 

    # bad credentials
    # username = "Test" 
    # password = "Test"

    external_port = int(os.getenv("EXTERNAL_PORT")) 

    subscriber = MQTTSubscriber(broker=public_IP, port=external_port, topic=topic, username=username, password=password)
    
    subscriber.start()
