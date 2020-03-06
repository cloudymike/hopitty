import paho.mqtt.client as mqtt
import ssl
import os

# This is the Publisher

IoT_protocol_name = "x-amzn-mqtt-ca"
aws_iot_endpoint = "a2d09uxsvr5exq-ats.iot.us-east-1.amazonaws.com" # <random>.iot.<region>.amazonaws.com
url = "https://{}".format(aws_iot_endpoint)

HOMEDIR=os.getenv("HOME")
if HOMEDIR is None:
    HOMEDIR = '/'
ca = HOMEDIR+"/secrets/certs/awsroot.crt" 
cert = HOMEDIR+"/secrets/certs/e27d28a42b-certificate.pem.crt"
private = HOMEDIR+"/secrets/keys/e27d28a42b-private.pem.key"


def ssl_alpn():
    try:
        #debug print opnessl version
        ssl_context = ssl.create_default_context()
        ssl_context.set_alpn_protocols([IoT_protocol_name])
        ssl_context.load_verify_locations(cafile=ca)
        ssl_context.load_cert_chain(certfile=cert, keyfile=private)

        return  ssl_context
    except Exception as e:
        print("exception ssl_alpn()")
        raise e



class socketclient():
    
    def __init__(self, host="localhost", maintopic="topic", connection=None):
        self.client = mqtt.Client()
        if connection == 'localhost':
            self.client.connect(host,1883,60)
        if connection == 'aws':
            ssl_context= ssl_alpn()
            self.client.tls_set_context(context=ssl_context)
            self.client.connect(aws_iot_endpoint, port=443)

        self.maintopic = maintopic
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.status = ""
        print("Starting mqtt client")
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
