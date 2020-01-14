#!/usr/bin/env python3
import time

import paho.mqtt.client as mqtt

# This is the Subscriber

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("topic/test")

def on_message(client, userdata, msg):
  if msg.payload.decode() == "Hello world!":
    print("Yes!")
    client.disconnect()
    
client = mqtt.Client()
client.connect("localhost",1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_start()

for i in range(19):
    print(i)
    time.sleep(1)

client.loop_stop()