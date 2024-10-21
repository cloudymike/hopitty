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
      t)
        TYPEOFEQUIPMENT="$OPTARG"
        ;;

  esac
done


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

python3 CreateTable.py
python3 LoadData.py
