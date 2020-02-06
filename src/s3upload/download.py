
import requests
import xml.dom.minidom
import xmltodict
import json


def downloadBeerSmith():
    i = requests.get('http://beersmithrecipes.s3-website.us-west-2.amazonaws.com/Cloud.bsmx')
    bsmxRawData = i.content
    bsmxCleanData = bsmxRawData.replace('&', 'AMP')
    #doc = xml.dom.minidom.parseString(bsmxCleanData)
    xmldict = xmltodict.parse(bsmxCleanData)
    return(xmldict)


if __name__ == "__main__":
    xmldict = downloadBeerSmith()

    recipes = xmldict['Cloud']['Data']['Cloud']
    for recipe in recipes:
        print(recipe['F_R_NAME'])

#    with open('data.txt', 'w') as outfile:
#        json.dump(xmldict, outfile)

