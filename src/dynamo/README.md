# Dynamodb of recipes

A dynamodb database that can be run either locally or remotely to keep all the recipes in staging format for direct loading by into brew controller.

## Schema
```
Item={
     'equipment_name': string,
     'recipe_name': string,
     'recipe_stages': {dict}
     }
```

* equipment_name is primary and partition key
* recipe_name is primary key
* recipe_stages json format dictionary that is directly loadable into brew controller.

## Local vs AWS
A local 
