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
        self.table = self.dynamodb.Table('hopittystatus')


    def fullstatus(self):
        try:
            response = self.table.get_item(Key={'hostname': 'dummyhost'})
        except ClientError as e:
            response = None
            print(e.response['Error']['Message'])
        if response and 'Item' in response:
            fs = response['Item']
            return(fs)
        else:
            return(response)

    def get_field(self, field):
        fullstatus = self.fullstatus()
        if not fullstatus:
            return(None)
        status = fullstatus['Payload']
        if field in status:
            return(status[field])
        else:
            return('')

    def get_state(self):
        return(self.get_field('state'))

    def get_equipmentname(self):
        return(self.get_field('equipmentname'))

    def get_stage(self):
        return(self.get_field('stage'))

    def get_recipename(self):
        return(self.get_field('recipename'))

    def get_controller_status(self):
        fullstatus = self.fullstatus()
        if not fullstatus:
            return(None)
        statusdict = fullstatus['Payload']
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
