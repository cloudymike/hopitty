# Dynamodb of recipes

A dynamodb database that can be run either locally or remotely to keep all the recipes in staging format for direct loading by into brew controller.

## Schema
```
Item={
     'equipment_name': string,
     'recipe_name': string,
     'stages': {dict}
     }
```

* equipment_name is primary and partition key
* recipe_name is primary key
* recipe_stages json format dictionary that is directly loadable into brew controller.

## Local vs AWS
A local version of dynamodb is available from Amazon as java code. This example  
uses this for development.


## Current two step process
Using the templates from AWS tutorial this set of code loads up a dynamodb database from
a json file that is created with this program: ../dynamorecipes.py.

This will allow these scripts to be completely independent of the code tree. It could all be combined
but be aware that this code requires python3
