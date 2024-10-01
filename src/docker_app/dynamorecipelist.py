import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
import json
import simplejson


class dynamorecipelist():
    def __init__(self, equipment_name='Grain 3G, HERMS, 5Gcooler, 5Gpot', dynamodb=None):
        self.equipmentname = equipment_name
        print('Equipment name set to {}'.format(self.equipmentname))
        if not dynamodb:
            self.dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
            print('dynamodb set to localhost')
        else:
            self.dynamodb = dynamodb
            print('dynamodb set to aws')



    def get_recipeNameList(self):
        table = self.dynamodb.Table('recipe4equipment')
        print("Table status:", table.table_status)
        recipeNameList = []
        lastkey = None
        while True:
            if lastkey:
                response = table.query(
                    KeyConditionExpression=Key('equipment_name').eq(self.equipmentname),
                    ExclusiveStartKey=lastkey
                )
            else:
                response = table.query(
                    KeyConditionExpression=Key('equipment_name').eq(self.equipmentname)
                )
            for recipe in response['Items']:
                recipeName = recipe['recipe_name']
                recipeNameList.append(recipeName)

            if 'LastEvaluatedKey' in response:
                lastkey = response['LastEvaluatedKey']
            else:
                break;

        return(recipeNameList)

    def set_equipmentname(self, equipmentname):
        if equipmentname:
            self.equipmentname = equipmentname
        print('Equipment name set to {}'.format(self.equipmentname))

    def get_stages(self, recipe_name, equipment_name):
        table = self.dynamodb.Table('recipe4equipment')
        try:
            response = table.get_item(Key={'equipment_name': equipment_name, 'recipe_name': recipe_name})
        except ClientError as e:
            print(e.response['Error']['Message'])
        if 'Item' in response:
            recipe2load = response['Item']
            return(recipe2load)
        else:
            return(None)

    def get_loadable_recipe(self, recipe_name, equipment_name):
        resp = self.get_stages(recipe_name, equipment_name)
        stages = resp['stages']
        recipename = resp['recipe_name']
        equipmentname = resp['equipment_name']
        recipedict = {}
        recipedict['stages'] = stages
        recipedict['recipename'] = recipename
        recipestr = simplejson.dumps(recipedict)
        return(recipestr)
