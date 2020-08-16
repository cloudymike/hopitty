import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key



class recipelist():
    def init(self, equipment_name='Grain 3G, HERMS, 5Gcooler, 5Gpot', dynamodb=None):
        self.equipmentname = equipment_name
        if not dynamodb:
            self.dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
        else:
            self.dynamodb = dynamodb
        

    def query_recipes(self):
    
        table = self.dynamodb.Table('recipe4equipment')
        response = table.query(
            KeyConditionExpression=Key('equipment_name').eq(self.equipmentname)
        )
        return response['Items']
    
    def get_recipeNameList(self):
        recipelist = self.query_recipes()
        recipeNameList = []
        for recipe in recipelist:
            recipeName = recipe['recipe_name']
            recipeNameList.append(recipeName)
        return(recipeNameList)

