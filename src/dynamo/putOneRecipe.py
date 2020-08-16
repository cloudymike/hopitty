from pprint import pprint
import boto3


def put_recipe(recipe_name, equipment_name, stages, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('recipe4equipment')
    response = table.put_item(
       Item={
            'equipment_name': equipment_name,
            'recipe_name': recipe_name,
            'stages': stages
        }
    )
    return response


if __name__ == '__main__':
    recipe_resp = put_recipe("Emptyrecipe", 'Noequipemnt',{})
    print("Put recipe succeeded:")
    pprint(recipe_resp)
