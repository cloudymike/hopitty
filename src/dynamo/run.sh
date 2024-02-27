#!/bin/bash

AWS=0
LOCAL=0
CLEAN=0
while getopts "h:aclt:" arg; do
  case $arg in
    h)
      echo "USAGE: $0 -achl "
      ;;
      c)
        CLEAN=1
        ;;
      a)
        AWS=1
        ;;
      l)
        LOCAL=1
        ;;
      t)
        TYPEOFEQUIPMENT="$OPTARG"
        ;;

  esac
done

if [ "$AWS" == "0" ] && [ "$LOCAL" == "0" ]
then
  echo "Either AWS or Local loading required"
  exit 1
fi


if [ "$CLEAN" == "1" ]
then
   rm -f ../out.json
   rm shared-local-instance.db
fi

if [ ! -f ../out.json ]
then
   pushd ..
   python2 dynamorecipes.py -u $USER -t "$TYPEOFEQUIPMENT"
   popd
fi



if [ ! -f localdynamodb/DynamoDBLocal.jar ] && [ "$LOCAL" == "1" ]
then
   mkdir -p localdynamodb
   pushd localdynamodb
   wget https://s3.us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_latest.tar.gz
   tar xvzf dynamodb_local_latest.tar.gz
   popd
fi

# Start local dynamodb
if [ "$LOCAL" == "1" ]
then
   java -Djava.library.path=./localdynamodb/DynamoDBLocal_lib -jar ./localdynamodb/DynamoDBLocal.jar -sharedDb &
   python3 CreateTable.py
   python3 LoadData.py
   read -p "Press any key to stop"
   kill -9 %1
else
   python3 CreateTable.py -a
   python3 LoadData.py -a
fi
