import boto3
import argparse


def create_recipe_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table_name  = 'recipe4equipment'
    table_names = [table.name for table in dynamodb.tables.all()]

    if table_name in table_names:
        table = dynamodb.Table('recipe4equipment')
    else:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'equipment_name',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'recipe_name',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'equipment_name',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'recipe_name',
                    'AttributeType': 'S'
                },

            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
    return table


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load recipedata into dynamodb')
    parser.add_argument('-a', '--aws', action='store_true', help='Use AWS dynamo')
    args = parser.parse_args()
    if args.aws:
        dynamodb = boto3.resource('dynamodb',region_name='us-east-1')
    else:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    recipe_table = create_recipe_table(dynamodb)
    print("Table status:", recipe_table.table_status)
