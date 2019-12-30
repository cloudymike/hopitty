import netsock
import time
import json
import argparse

stages={}
stages['s1'] = {}
stages['s1']['cycles'] = 3
stages['s2'] = {}
stages['s2']['cycles'] = 4



if __name__ == "__main__":
    
    
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-n", "--netsock", action='store_true', help='Use netsock communication')
    group.add_argument("-m", "--mqtt", action='store_true', help='Use mqtt communication')
    args = parser.parse_args()
    
    if args.netsock:
        client = netsock.socketclient()
    
    
    data = client.write('status')
    print('Received {}'.format(data))
    assert 'stop' in data
    data = client.write('run')
    print('Received {}'.format(data))
    time.sleep(3)
    data = client.write('status')
    print('Received {}'.format(data))
    assert 'run' in data
    time.sleep(1)
    data = client.write('pause')
    print('Received {}'.format(data))
    data = client.write('status')
    print('Received {}'.format(data))
    assert 'pause' in data
    time.sleep(1)
    data = client.write('status')
    print('Received {}'.format(data))
    data = client.write('run')
    print('Received {}'.format(data))
    time.sleep(3)
    data = client.write('status')
    print('Received {}'.format(data))
    assert 'run' in data
    data = client.write(json.dumps(stages))
    time.sleep(1)
    data = client.write('status')
    print('Received {}'.format(data))
    assert 'stop' in data
    data = client.write('run')
    time.sleep(1)
    data = client.write('status')
    print('Received {}'.format(data))
    assert 's1' in data
    time.sleep(3)
    data = client.write('status')
    print('Received {}'.format(data))
    assert 's2' in data

    time.sleep(4)
    data = client.write('status')
    print('Received {}'.format(data))
    assert 'holdforever' in data

    data = client.write('terminate')
    print("Program should be terminated")
