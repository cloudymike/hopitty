#!/bin/bash

# Start local dynamodb
java -Djava.library.path=~/dynamodb/DynamoDBLocal_lib -jar ~/dynamodb/DynamoDBLocal.jar -sharedDb &

# Check that dynamodb is working locally
aws dynamodb list-tables --endpoint-url http://localhost:8000

#Load up database
python3 CreateTable.py
python3 LoadData.py
python3 QueryByEquipment.py
python3 GetRecipe.py
python3 putOneRecipe.py


kill -9 %1
