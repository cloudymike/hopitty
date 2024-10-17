#!/bin/bash

USER=5399
TYPEOFEQUIPMENT="Grain 3G, 5Gcooler, 5Gpot, mashexittemp"

OUTPUTFILE=/tmp/test.bsmx
rm -f $OUTPUTFILE
# Find all recipies that are public by USER
# Should really loop until empty. Each batch is 20 recipies

LIST0=$(curl -s https://beersmithrecipes.com/listrecipes/5399/0 | grep viewrecipe | cut -d/ -f5) 
LIST1=$(curl -s https://beersmithrecipes.com/listrecipes/5399/1 | grep viewrecipe | cut -d/ -f5) 

LIST="$LIST0 $LIST1"
for RECIPEID in $LIST1 
do
	echo $RECIPEID
	wget -qO - https://beersmithrecipes.com/download.php?id=$RECIPEID >> $OUTPUTFILE

done

# Remember to use venv from top level....
# source ../../venv/bin/activate
pushd ..
python2 dynamorecipes.py -b /tmp/test.bsmx -t "$TYPEOFEQUIPMENT"
popd
