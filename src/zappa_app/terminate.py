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

# Callback when connection is accidentally lost.
def on_connection_interrupted(connection, error, **kwargs):
    print("Connection interrupted. error: {}".format(error))


# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

    if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
        print("Session did not persist. Resubscribing to existing topics...")
        resubscribe_future, _ = connection.resubscribe_existing_topics()

        # Cannot synchronously wait for resubscribe result because we're on the connection's event-loop thread,
        # evaluate result with a callback instead.
        resubscribe_future.add_done_callback(on_resubscribe_complete)


def on_resubscribe_complete(resubscribe_future):
        resubscribe_results = resubscribe_future.result()
        print("Resubscribe results: {}".format(resubscribe_results))

        for topic, qos in resubscribe_results['topics']:
            if qos is None:
                sys.exit("Server rejected resubscribe to topic: {}".format(topic))


def terminate():
    # Spin up resources
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

    HOMEDIR=os.getenv("HOME")
    r = requests.get('https://www.amazontrust.com/repository/AmazonRootCA1.pem')
    cabuf= r.text
    cert = HOMEDIR+"/secrets/certs/e27d28a42b-certificate.pem.crt"
    certbuf = os.environ.get("IOT_CERT", None)
    private = HOMEDIR+"/secrets/keys/e27d28a42b-private.pem.key"
    privatebuf = os.environ.get("IOT_PRIVATE", None)

    aws_iot_endpoint = "a2d09uxsvr5exq-ats.iot.us-east-1.amazonaws.com" # <random>.iot.<region>.amazonaws.com
    client_id='hopitty'
    topic = 'topic/test'
    message='terminate'



    mqtt_connection = mqtt_connection_builder.mtls_from_bytes(
            endpoint=aws_iot_endpoint,
            cert_bytes= str.encode(certbuf),
            pri_key_bytes=str.encode(privatebuf),
            client_bootstrap=client_bootstrap,
            rootca_buffer=cabuf,
            client_id='hopitty')

    print("Connecting to {} with client ID '{}'...".format(
        aws_iot_endpoint, client_id))

    connect_future = mqtt_connection.connect()
    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")

    mqtt_connection.publish(
        topic=topic,
        payload=message,
        qos=mqtt.QoS.AT_LEAST_ONCE)

    print("Disconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")
    return('Terminating client {}'.format(client_id))

if __name__ == '__main__':
    terminate()
