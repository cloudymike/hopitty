#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='vostro'))
channel = connection.channel()

q = channel.queue_declare(queue='hello')

consumers = q.method.consumer_count

print "Consumers: ", consumers

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')


print(" [x] Sent 'Hello World!'")
connection.close()

