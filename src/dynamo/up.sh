#!/bin/bash

if [ ! -f ../out.json ]
then
   pushd ..
   python dynamorecipes.py -d
   popd
fi



if [ ! -f localdynamodb/DynamoDBLocal.jar ]
then
   mkdir -p localdynamodb
   pushd localdynamodb
   wget https://s3.us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_latest.tar.gz
   tar xvzf dynamodb_local_latest.tar.gz 
   popd
fi

# Start local dynamodb
java -Djava.library.path=./localdynamodb/DynamoDBLocal_lib -jar ./localdynamodb/DynamoDBLocal.jar -sharedDb &

# Check that dynamodb is working locally
aws dynamodb list-tables --endpoint-url http://localhost:8000

#Load up database
python3 CreateTable.py
python3 LoadData.py


read -p "Press any key to stop"

kill -9 %1
