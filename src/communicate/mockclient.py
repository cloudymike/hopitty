import netsock
import time
import json

stages={}
stages['s1'] = {}
stages['s1']['cycles'] = 3
stages['s2'] = {}
stages['s2']['cycles'] = 4



if __name__ == "__main__":
    data = netsock.write('status')
    print('Received {}'.format(data))
    assert 'stop' in data
    data = netsock.write('run')
    print('Received {}'.format(data))
    time.sleep(3)
    data = netsock.write('status')
    print('Received {}'.format(data))
    assert 'run' in data
    time.sleep(1)
    data = netsock.write('pause')
    print('Received {}'.format(data))
    data = netsock.write('status')
    print('Received {}'.format(data))
    assert 'pause' in data
    time.sleep(1)
    data = netsock.write('status')
    print('Received {}'.format(data))
    data = netsock.write('run')
    print('Received {}'.format(data))
    time.sleep(3)
    data = netsock.write('status')
    print('Received {}'.format(data))
    assert 'run' in data
    data = netsock.write(json.dumps(stages))
    time.sleep(1)
    data = netsock.write('status')
    print('Received {}'.format(data))
    assert 'stop' in data
    data = netsock.write('run')
    time.sleep(1)
    data = netsock.write('status')
    print('Received {}'.format(data))
    assert 's1' in data
    time.sleep(3)
    data = netsock.write('status')
    print('Received {}'.format(data))
    assert 's2' in data

    time.sleep(4)
    data = netsock.write('status')
    print('Received {}'.format(data))
    assert 'holdforever' in data

    data = netsock.write('terminate')
    print("Program should be terminated")
