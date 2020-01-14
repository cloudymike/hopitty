import netsock
import mqttsock

import time
import json
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-n", "--netsock", action='store_true', help='Use netsock communication')
    group.add_argument("-m", "--mqtt", action='store_true', help='Use mqtt communication')
    args = parser.parse_args()
    if args.netsock:
        client = netsock.socketclient() 
    if args.mqtt:
        client = mqttsock.socketclient()
    # Wait for a message to appear
    time.sleep(2)
    
    data = client.read_status()
    status_string = str(data).replace("'","")
    status_dict = json.loads(status_string)
    print('Status==> {}'.format(status_dict['status']))
    client.stop()