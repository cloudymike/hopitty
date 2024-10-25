from decimal import Decimal
import json
import boto3
import argparse


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
    parser = argparse.ArgumentParser(description='Load recipedata into dynamodb')
    parser.add_argument('-a', '--aws', action='store_true', help='Use AWS dynamo')
    parser.add_argument('-D', '--Dynamodb', default=None, type=str, help='URL for dynamoDB ')
    args = parser.parse_args()
    if args.aws:
        dynamodb = boto3.resource('dynamodb',region_name='us-east-1')
    elif args.Dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url=args.Dynamodb, region_name='us-east-2')
        print("Dynamodb on {}".format(args.Dynamodb))
    else:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    with open("../out.json") as json_file:
        recipe_list = json.load(json_file, parse_float=Decimal)
    load_recipes(recipe_list, dynamodb)
