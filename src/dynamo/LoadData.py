from decimal import Decimal
import json
import boto3


def load_recipes(recipes, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('recipe4equipment')
    for recipe in recipes:
        equipment_name = recipe['equipment_name']
        recipe_name = recipe['recipe_name']
        print("Adding recipe {} for equipment {}".format(recipe_name, equipment_name))
        table.put_item(Item=recipe)


if __name__ == '__main__':
    with open("../out.json") as json_file:
        recipe_list = json.load(json_file, parse_float=Decimal)
        print(recipe_list)
    load_recipes(recipe_list)
