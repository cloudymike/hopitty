import netsock
import time
import json

if __name__ == "__main__":
    status_string = str(netsock.write('status')).replace("'","")
    status_dict = json.loads(status_string)
    print('Stage {}'.format(status_dict['stage']))
