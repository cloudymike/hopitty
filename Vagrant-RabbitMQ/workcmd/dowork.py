#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='workpkg')

channel.basic_publish(exchange='',
                      routing_key='workpkg',
                      body='Start working!')
print(" [x] Sent 'Start working!'")
connection.close()
