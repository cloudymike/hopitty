#!/usr/bin/env python
import pika
import sys
rabbithost = 'localhost'
workconnection = pika.BlockingConnection(pika.ConnectionParameters(
            host=rabbithost))
workchannel = workconnection.channel()

q = workchannel.queue_declare(queue='workpkg')

consumers = q.method.consumer_count
workconnection.close()

print "Workers connected: ", consumers


if consumers != 1:
    sys.exit(1)