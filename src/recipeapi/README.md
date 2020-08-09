#API to get stages version of recipe

An API that will get a recipe as a staging json with the recipename as a key (possibly url encoded).

Available recipes can be listed in full or based on recipes matching a specific
equipment name (possibly url encoded). All return values are in json format.

## Routes

### /list
Provide a list of all recipes

### /list/<equipmentname>
List of all recipes that matches that equipment name. The equipment name needs to be url encoded

### /recipe/<equipmentname>/<recipename>
Recipe in staging format (json) for the equipment listed. Equipmentname and Recipename will be url encoded.

## Direct read from xml or store first to dynamodb

### Store to DynamoDB
We already have a recipe list in mysql, a template to follow.

A more compelling reason though is that we can also run the full recipe test and create a list of not just matching names but also validated recipes. This is already done in threadscan
but just for one type of equipment. We need to loop over the equipment list.

Currently we check the equipment in the recipe against the equipment name but then we check against the parameters. Currently there is just one valid equipment for each recipe. A recipe could be valid for multiple equipments and may be different if we remove the hard check as intended. Thus we should stay on that path and include equipment and recipe when requesting a recipe.
