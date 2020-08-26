from pprint import pprint
import boto3
from botocore.exceptions import ClientError

class dynamostatus():
    def __init__(self, dynamodb=None):
        if not dynamodb:
            self.dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
            print('dynamodb set to localhost')
        else:
            self.dynamodb = dynamodb

    def fullstatus(self):
        table = self.dynamodb.Table('hopittystatus')
        try:
            response = table.get_item(Key={'hostname': 'dummyhost'})
        except ClientError as e:
            response = None
            print(e.response['Error']['Message'])
        if response and 'Item' in response:
            fs = response['Item']
            return(fs)
        else:
            return(response)

    def get_state(self):
        possible = ['terminate','pause','run', 'stop', 'skip']
        fullstatus = self.fullstatus()
        status = fullstatus['Payload']
        state = status['state']
        return(state)

def get_equipmentname():
    return('Some equipment')

def get_stage():
    return('current state')

def get_recipename():
    return('current recipe name')

def get_controller_status(self):
    statusdict = {}
    data = statusdict['status']

    ctrlmatrix = []
    for appliance, currstatus in data.items():
        actual = str(currstatus['actual'])
        if currstatus['active']:
            target = str(currstatus['target'])
        else:
            target = ''
        unit = currstatus['unit']
        ctrlrow = [appliance,actual,target,unit]
        ctrlmatrix.append(ctrlrow)
    return(ctrlmatrix)


if __name__ == '__main__':
    dynamodb = boto3.resource('dynamodb',region_name='us-east-1')
    statusdb = dynamostatus(dynamodb)
    full = statusdb.fullstatus()
    print(full)
    print('State: {}'.format(statusdb.get_state()))
