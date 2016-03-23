#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='commands')
message = ' '.join(sys.argv[1:]) or "info: Hello World!"

channel.basic_publish(exchange='',
                      routing_key='commands',
                      body=message)
print(" [x] Sent ", message)
connection.close()
