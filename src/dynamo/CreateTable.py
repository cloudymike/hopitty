import boto3


def create_recipe_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.create_table(
        TableName='recipe4equipment',
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
    recipe_table = create_recipe_table()
    print("Table status:", recipe_table.table_status)
