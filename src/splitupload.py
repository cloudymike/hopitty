#!/usr/bin/python
import logging
import boto3
from botocore.exceptions import ClientError
import argparse
import recipeModel
import sys
import json

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def upload_string(content, bucket, object_name):
    """Upload a file to an S3 bucket

    :param content: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. 
    :return: True if file was uploaded, else False
    """

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True





if __name__ == "__main__":
    bsmxfile='/home/mikael/.beersmith3/Cloud.bsmx'
    print("Uploading full file")
    upload_file(bsmxfile,'beersmithrecipes','Cloud.bsmx')

    print("Creating a list of recipes")
    rl = recipeModel.RecipeList()
    rl.readBeerSmith(bsmxfile)
    iterlist = rl.getlist()
    s3_client = boto3.client('s3')
    recipeEquipment = {}

    index = '''<html>
               <header><title>Recipe list</title></header>
               <body>'''

    print("Uploading individual recipes")
    for recipeName in iterlist:
        print("Uploading {}".format(recipeName))
        content = rl.getRecipe(recipeName)
        recipeEquipment[content.name] = content.equipment
        index = index + '<p>{}</p>\n'.format(recipeName)
        s3_client.put_object(Body=content.bsmx, Bucket='beersmithrecipes', Key='{}.bsmx'.format(recipeName))

    print("Upload recipe name to equipment json")
    index = index + '</body></html>\n'
    s3_client.put_object(Body=str(index), Bucket='beersmithrecipes', Key='index.html')
    jrE = json.dumps(recipeEquipment)
    s3_client.put_object(Body=str(jrE), Bucket='beersmithrecipes', Key='recipeEquipment.json')

