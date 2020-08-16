from pprint import pprint
import boto3
from botocore.exceptions import ClientError


def get_recipe(recipe_name, equipment_name, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('recipe4equipment')

    try:
        response = table.get_item(Key={'equipment_name': equipment_name, 'recipe_name': recipe_name})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        if 'Item' in response:
            return response['Item']

def NumberOfStages(recipe):
    number = 0
    if 'stages' not in recipe:
        return(0)
    for key in recipe['stages']:
        number = number + 1
    return(number)

if __name__ == '__main__':
    recipe = get_recipe("193 Herms Kolsch", 'Grain 3G, HERMS, 5Gcooler, 5Gpot',)
    if recipe:
        print("Get recipe succeeded:")
        print('Stages in recipe: {}'.format(NumberOfStages(recipe)))
        #pprint(recipe)
