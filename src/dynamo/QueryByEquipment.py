import boto3
from boto3.dynamodb.conditions import Key


def query_recipes(equipment_name, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('recipe4equipment')
    response = table.query(
        KeyConditionExpression=Key('equipment_name').eq(equipment_name)
    )
    return response['Items']


if __name__ == '__main__':
    query_equipment = 'Grain 3G, HERMS, 5Gcooler, 5Gpot'
    print('Recipes using equipment {}'.format(query_equipment))
    recipes = query_recipes(query_equipment)
    for recipe in recipes:
        print('    |{}|'.format(recipe['recipe_name']))
