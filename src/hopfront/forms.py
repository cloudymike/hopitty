from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import DataRequired
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key


#==== Exportables
def query_recipes(equipment_name='Grain 3G, HERMS, 5Gcooler, 5Gpot', dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('recipe4equipment')
    response = table.query(
        KeyConditionExpression=Key('equipment_name').eq(equipment_name)
    )
    return response['Items']


#======== End exportables

def recipe_choices():
    recipelist = query_recipes()
    recipeNameList = []
    recipeNameStr = ''
    for recipe in recipelist:
        recipeName = recipe['recipe_name']
        stages = recipe['stages']
        recipeTuple = (recipeName,recipeName)
        recipeNameList.append(recipeTuple)
        print(recipeName)
    #return([('porter','porter'),('saison','saison'),('IPA','IPA'),('NEIPA','NEIPA'),('wit','wit')])
    return(recipeNameList)


class CmdForm(FlaskForm):

    #command = StringField('Command', validators=[DataRequired()])
    command = RadioField('Command', choices=[('stop','stop'),('run','run'),('pause','pause'),('skip','skip'),('terminate','terminate')])
    submit = SubmitField('Execute')
    
class LoadForm(FlaskForm):
    load = StringField('Stages json', validators=[DataRequired()])
    submit = SubmitField('Execute')
    
class RecipeForm(FlaskForm):
   #choices=[('porter','porter'),('saison','saison'),('IPA','IPA'),('NEIPA','NEIPA'),('wit','wit')]
    choices = recipe_choices()
    recipe = RadioField('Recipe', choices=choices)
    submit = SubmitField('Select')
    
