# app.py

from flask import Flask
from flask import jsonify
import xmltodict
import requests
import boto3

# Initialize dynamodb access
dynamodb = boto3.resource('dynamodb')
db = dynamodb.Table('zappatutorial')



app = Flask(__name__)

@app.route('/')
def hello_world():
 return '<h1>Hey there people I am Bobby Brown</h1><p>Moving to Montana</p>'

def downloadBeerSmith():
    i = requests.get('http://beersmithrecipes.s3-website.us-west-2.amazonaws.com/Cloud.bsmx')
    bsmxRawData = i.content.decode("utf-8")
    bsmxCleanData = bsmxRawData.replace('&', 'AMP')
    xmldict = xmltodict.parse(bsmxCleanData)
    return(xmldict)


@app.route('/list')
def list():
    xmldict = downloadBeerSmith()

    recipes = xmldict['Cloud']['Data']['Cloud']
    recipelist = []
    for recipe in recipes:
        oneEntry = {}
        oneEntry['name'] = recipe['F_R_NAME']
        oneEntry['equipment'] = recipe['F_R_EQUIP_NAME']
        recipelist.append(oneEntry)

    return jsonify(recipelist)


@app.route('/counter', methods=['GET'])
def counter_get():
    res = db.get_item(Key={'id': 'counter'})
    testval = res['Item']['testval']
    counter_value = str(res['Item']['counter_value'])
    jsonval = jsonify({'testval': testval, 'counter_value': counter_value})
    return(jsonval)

@app.route('/counter/increase', methods=['POST'])
def counter_increase():
    res = db.get_item(Key={'id': 'counter'})
    value = res['Item']['counter_value'] + 1
    res = db.update_item(
        Key={'id': 'counter'},
        UpdateExpression='set counter_value=:value',
        ExpressionAttributeValues={':value': value},
        )
    strvalue = str(value)
    return jsonify({'counter': strvalue})

# We only need this for local development.
if __name__ == '__main__':
 app.run()
