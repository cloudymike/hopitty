#!/bin/bash

# Remember to use venv from top level....
# source ../../venv/bin/activate

cd /hopitty/src/onlinebeersmith

USER=5399
TYPEOFEQUIPMENT="Grain 3G, 5Gcooler, 5Gpot, mashexittemp"

JSONDIR=/tmp/tmpjsonrecipies

while true
do
	rm -rf $JSONDIR
	mkdir $JSONDIR

	# Find all recipies that are public by USER
	# Should really loop until empty. Each batch is 20 recipies
	LIST0=$(curl -s https://beersmithrecipes.com/listrecipes/5399/0 | grep viewrecipe | cut -d/ -f5) 
	LIST1=$(curl -s https://beersmithrecipes.com/listrecipes/5399/1 | grep viewrecipe | cut -d/ -f5) 

	LIST="$LIST0 $LIST1"
	for RECIPEID in $LIST 
	do
		echo $RECIPEID
		rm -f /tmp/tmp.bsmx
		wget -qO - https://beersmithrecipes.com/download.php?id=$RECIPEID > /tmp/tmp.bsmx

		pushd ..
		python3 dynamorecipes.py -b /tmp/tmp.bsmx -f $JSONDIR/$RECIPEID.json -t "$TYPEOFEQUIPMENT"
		popd

	done

	cat $JSONDIR/*.json | jq -s 'add' > ../out.json
	echo "====================================== Current output file ========================================"
	jq .[].recipe_name ../out.json
	pushd ../dynamo
	python3 CreateTable.py -D "http://dynamodb:8000"
	python3 LoadData.py -D "http://dynamodb:8000"
	popd

	sleep 600
done