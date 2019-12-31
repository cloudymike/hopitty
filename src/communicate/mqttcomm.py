import paho.mqtt.client as mqtt

# This is the Publisher

client = mqtt.Client()
client.connect("localhost",1883,60)
client.publish("topic/test", "Hello world!");
client.disconnect();


class socketclient():
    
    def __init__(self, host="localhost", maintopic="topic"):
        self.client = mqtt.Client()
        self.client.connect(host,1883,60)
        self.maintopic = maintopic


    def write_command(self, command, subtopic='test'):
        topic = self.maintopic+"/"+subtopic
        self.client.publish(topic, command)
        return('ok')
    
