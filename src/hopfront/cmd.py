#!/usr/bin/python


import netsock
import mqttsock
import time
import argparse
import json

stages={}
stages['s1'] = {}
stages['s1']['cycles'] = 3
stages['s2'] = {}
stages['s2']['cycles'] = 4


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Issue a command to a running server')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-n", "--netsock", action='store_true', help='Use netsock communication')
    group.add_argument("-m", "--mqtt", action='store_true', help='Use mqtt communication')
    group.add_argument("-a", "--aws", action='store_true', help='Use aws mqtt communication')
    parser.add_argument('command', choices=['terminate', 'run', 'stop', 'pause', 'skip', 'load', 'status'], help='Command to run')
    args = parser.parse_args()

    if args.netsock:
        client = netsock.socketclient() 
    if args.mqtt:
        client = mqttsock.socketclient(connection='localhost') 
    if args.aws:
        client = mqttsock.socketclient(connection='aws')
        
    time.sleep(2)

    if args.command == 'load':
        data = client.write_command(json.dumps(stages))
    elif args.command == 'status':
        data = client.read_status()
        status_string = str(data).replace("'","")
        status_dict = json.loads(status_string)
        print('Status==> {}'.format(status_dict['status']))
    else:
        data = client.write_command(args.command)
    print("Program received command {}".format(args.command))
    client.stop()