import mqttsock
import sys
import json
import time
import requests
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

class brewque():

    def __init__(self, connection=None):
        self.comm_client = mqttsock.socketclient(connection=connection)
        print('Connection is {}'.format(connection))

    def get_state(self):
        try:
            current_status = self.comm_client.read_status()
            status_string = str(current_status).replace("'","")
            statusdict = json.loads(status_string)
            current_state = statusdict['state']
        except:
            print('Can not communicate with controller')
            current_status = 'Controller failing'
            current_state = "stop"
        return(current_state)

    def get_status(self):
        try:
            current_status = self.comm_client.read_status()
        except:
            print('Can not communicate with controller')
            current_status = 'Controller failing'
        return(current_status)

    def put_recipe(self,data):
        try:
            result = self.comm_client.write_command(data)
        except:
            print('Can not communicate with controller')

    def put_command(self,data):
        try:
            result = self.comm_client.write_command(data)
        except:
            print('Can not communicate with controller')

    def get_recipename(self):
        try:
            current_status = self.comm_client.read_status()
        except:
            print('Can not communicate with controller')
            current_status = None
        if current_status:
            statusdict = json.loads(current_status)
            if 'recipename' in statusdict:
                return(statusdict['recipename'])
            else:
                return('')

    def get_equipmentname(self):
        try:
            current_status = self.comm_client.read_status()
        except:
            print('Can not communicate with controller')
            current_status = None
        if current_status:
            statusdict = json.loads(current_status)
            if 'equipmentname' in statusdict:
                equipmentname = statusdict['equipmentname']
            else:
                equipmentname = ''
            return(equipmentname)

    def get_controller_status(self):
        try:
            current_status = self.comm_client.read_status()
            status_string = str(current_status).replace("'","")
            statusdict = json.loads(status_string)
            data = statusdict['status']
        except:
            print('Can not communicate with controller')
            data = None

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
