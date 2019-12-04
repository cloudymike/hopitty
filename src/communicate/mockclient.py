import netsock
import time

if __name__ == "__main__":
    data = netsock.writeSocket('status')
    print('Received {}'.format(data))
