import boto3
import argparse


def create_recipe_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table_name = 'recipe4equipment'
    existing_tables = dynamodb_client.list_tables()['TableNames']
    if table_name in existing_tables:
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
    parser.add_argument('-d', '--dynamoendpoint', default=None, help='Dynamodb endpoint to use')
    args = parser.parse_args()
    recipe_table = create_recipe_table(args.dynamoendpoint)
    print("Table status:", recipe_table.table_status)
