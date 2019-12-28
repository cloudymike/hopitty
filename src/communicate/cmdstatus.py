import netsock
import time

if __name__ == "__main__":
    data = netsock.write('status')
    print('Received {}'.format(data))
import netsock
import time
import json

if __name__ == "__main__":
    data = netsock.write('status')
    datadict = json.loads(data)
    print('Stage {}'.format(datadict['stage']))
