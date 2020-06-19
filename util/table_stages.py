import numpy as np
import matplotlib.pyplot as plt
import json
import argparse
import sys

def rowprint(row):
    width=6
    s=''
    for x in row:
        s=s+'|{}'.format(str(x)[:width].ljust(width))
    s=s+'|'
    print(s)

def tablePrint(collabel,rowlabel,clust_data):
    collabel = ['stage'] + collabel
    rowprint(collabel)
    i = 0
    for row in clust_data:
        row = [rowlabel[i]] + row
        i = i + 1
        rowprint(row)


parser = argparse.ArgumentParser(description='Read a stages file and create a table')
parser.add_argument('-f', '--file', required=True, help='Input JSON file')
parser.add_argument('-t', '--terminal', action='store_true', help='Output to termnial')
args = parser.parse_args()



with open(args.file) as json_file:
    data = json.load(json_file)


for stage, appliances in data.items():
    collabel = []
    for appliance, action in appliances.items() :
        collabel.append(appliance)
    break

collabel.sort()
noOfCol = len(collabel)

clust_data = []
rowlabel = []
for stage, appliances in sorted(data.items()):
    row = []
    rowlabel.append(stage)
    for i in range(0,noOfCol):
        if appliances[collabel[i]]['active']:
            row.append(action['targetValue'])
        else:
            row.append(' ')
    clust_data.append(row)

if args.terminal:
    tablePrint(collabel,rowlabel,clust_data)
else:
# Try to display if fail just raw print it
    try:
        plt.axis('tight')
        plt.axis('off')
        the_table = plt.table(cellText=clust_data,colLabels=collabel,rowLabels=rowlabel,loc='center')
        plt.show()
    except:
        tablePrint(collabel,rowlabel,clust_data)


