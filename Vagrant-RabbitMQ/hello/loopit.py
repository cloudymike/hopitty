#!/usr/bin/env python
import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

while True:
  method_frame, header_frame, body = channel.basic_get('hello')
  if method_frame:
      print('----', body)
      channel.basic_ack(method_frame.delivery_tag)
  else:
      print(' [*] ')
  time.sleep(1)
