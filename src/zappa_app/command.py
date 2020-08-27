# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from __future__ import absolute_import
from __future__ import print_function
import argparse
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import sys
import threading
import time
from uuid import uuid4
import os
import requests

def command(message):
    # Spin up resources
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

    certbuf = os.environ.get("IOT_CERT", None)
    privatebuf = os.environ.get("IOT_PRIVATE", None)

    aws_iot_endpoint = "a2d09uxsvr5exq-ats.iot.us-east-1.amazonaws.com" # <random>.iot.<region>.amazonaws.com
    client_id='hopitty'
    topic = 'topic/test'

    mqtt_connection = mqtt_connection_builder.mtls_from_bytes(
            endpoint=aws_iot_endpoint,
            cert_bytes= str.encode(certbuf),
            pri_key_bytes=str.encode(privatebuf),
            client_bootstrap=client_bootstrap,
            client_id='hopitty')

    connect_future = mqtt_connection.connect()
    # Future.result() waits until a result is available
    connect_future.result()

    mqtt_connection.publish(
        topic=topic,
        payload=message,
        qos=mqtt.QoS.AT_LEAST_ONCE)

    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")
    return('Command {} sent to client {}'.format(message, client_id))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run brew equiipment with communication enabled for control.')
    parser.add_argument('-c', '--command', required=True, type=str, help='Command to execute')
    args = parser.parse_args()
    if args.command:
        command(args.command)
