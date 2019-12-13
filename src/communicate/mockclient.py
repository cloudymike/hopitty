import netsock
import time

if __name__ == "__main__":
    data = netsock.writeSocket('status')
    print('Received {}'.format(data))
    assert 'stop' in data
    data = netsock.writeSocket('run')
    print('Received {}'.format(data))
    time.sleep(3)
    data = netsock.writeSocket('status')
    print('Received {}'.format(data))
    assert 'run' in data
    time.sleep(1)
    data = netsock.writeSocket('pause')
    print('Received {}'.format(data))
    data = netsock.writeSocket('status')
    print('Received {}'.format(data))
    assert 'pause' in data
    time.sleep(1)
    data = netsock.writeSocket('status')
    print('Received {}'.format(data))
    data = netsock.writeSocket('run')
    print('Received {}'.format(data))
    time.sleep(3)
    data = netsock.writeSocket('status')
    print('Received {}'.format(data))
    assert 'run' in data
    time.sleep(1)
    data = netsock.writeSocket('terminate')
    print("Program should be stopped")
