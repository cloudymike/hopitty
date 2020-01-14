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
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.status = ""

        self.client.loop_start()
        
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe(self.maintopic+"/status")

    def on_message(self, client, userdata, msg):
        self.status = msg.payload.decode()

    def write_command(self, command, subtopic='test'):
        topic = self.maintopic+"/"+subtopic
        self.client.publish(topic, command)
        return('ok')
        
    def read_status(self):
        return(self.status)
    

    def stop(self):
      self.client.loop_stop()
