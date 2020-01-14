import netsock
import mqttsock
import time
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
        
    data = client.write_command('pause')
    print("Program should be paused")
    client.stop()