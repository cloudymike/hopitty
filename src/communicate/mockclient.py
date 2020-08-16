import netsock
import mqttsock
import time
import json
import argparse

stages={}
stages['s1'] = {}
stages['s1']['cycles'] = 4
stages['s2'] = {}
stages['s2']['cycles'] = 4



if __name__ == "__main__":


    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-n", "--netsock", action='store_true', help='Use netsock communication')
    group.add_argument("-m", "--mqtt", action='store_true', help='Use mqtt communication')
    group.add_argument("-a", "--aws", action='store_true', help='Use aws mqtt communication')
    args = parser.parse_args()

    if args.netsock:
        client = netsock.socketclient()
    if args.mqtt:
        client = mqttsock.socketclient(connection='localhost')
        # Wait for a message to appear
        time.sleep(2)
    if args.aws:
        client = mqttsock.socketclient(connection='aws')
        # Wait for a message to appear
        time.sleep(2)


    data = client.read_status()
    print('Received {}'.format(data))
    assert 'stop' in data

    data = client.write_command(json.dumps(stages))
    time.sleep(3)
    data = client.read_status()
    print('Received {}'.format(data))
    assert 'stop' in data

    data = client.write_command('run')
    print('Received {}'.format(data))
    time.sleep(3)
    data = client.read_status()
    print('Received {}'.format(data))
    assert 'run' in data

    data = client.write_command('pause')
    print('Received {}'.format(data))
    time.sleep(3)
    data = client.read_status()
    print('Received {}'.format(data))
    assert 'pause' in data

    data = client.write_command('run')
    print('Received {}'.format(data))
    time.sleep(3)
    data = client.read_status()
    print('Received {}'.format(data))
    assert 'run' in data

    data = client.write_command(json.dumps(stages))
    time.sleep(3)
    data = client.read_status()
    print('Received {}'.format(data))
    assert 'stop' in data

    data = client.write_command('run')
    time.sleep(2)
    data = client.read_status()
    print('Received {}'.format(data))
    assert 's1' in data
    data = client.write_command('pause')
    print('Received {}'.format(data))
    time.sleep(3)
    data = client.read_status()
    print('Received {}'.format(data))
    assert 'pause' in data
    assert 's1' in data

    data = client.write_command('skip')
    time.sleep(1)
    data = client.read_status()
    print('Received {}'.format(data))
    assert 's2' in data

    time.sleep(2)
    data = client.read_status()
    print('Received {}'.format(data))
    time.sleep(2)
    data = client.read_status()
    print('Received {}'.format(data))
    time.sleep(2)
    data = client.read_status()
    print('Received {}'.format(data))
    #assert 'stop' in data

    data = client.write_command('terminate')

    client.stop()
    print("Program should be terminated")
