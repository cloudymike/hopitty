import netsock
import time

if __name__ == "__main__":
    data = netsock.write('status')
    print('Received {}'.format(data))
