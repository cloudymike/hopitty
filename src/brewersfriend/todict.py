import xmltodict
import argparse

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-b', '--bsmx', default=None, help='Beersmith file to use, bsmx format, ')
group.add_argument('-f', '--brewersfriend', default=None, help='Brewers friend file to use, xml format, ')

args = parser.parse_args()

if args.bsmx:
    with open(args.bsmx) as fd:
        dict = xmltodict.parse(fd.read())
    recipename=dict['Recipes']['Data']['Recipe']['F_R_NAME']

if args.brewersfriend:
    with open(args.brewersfriend) as fd:
        dict = xmltodict.parse(fd.read())
    recipename=dict['RECIPES']['RECIPE']['NAME']


#print(dict)
print("Recipe name: {}".format(recipename))