import paho.mqtt.client as mqtt

class MQTTSubscriber:
    def __init__(self, broker:int, port:int, topics=[]):
        '''Constructor for the MQTT subscriber class
        Args:
            broker {int} -- IP address for the broker/proxy to connect to
            port {int} -- port to run the subscriber process on

        Kwargs:
            topics {List[str]} -- list of topics the subscriber should initally subscribe to

        Returns:
            None
        '''
        if broker is None or type(broker) != int:
            raise TypeError("Broker argument is required and must be an integer")
        if port is None or type(port) != int:
            raise TypeError("Port argument is required and must be an integer")
        

        self.topics = topics

    def add_topic(self, topic):
        '''Add a topic to the subscriber instnace
        Args:
            topic {str} -- name of the new topic to subscribe to

        Kwargs:
            None
            
        Returns:
            None
        '''
        self.topics.append(topic)

if __name__ == "__main__":
    subscriber = MQTTSubscriber()
