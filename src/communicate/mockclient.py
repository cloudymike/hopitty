import netsock
import time

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
    time.sleep(1)
    data = netsock.write('terminate')
    print("Program should be stopped")
