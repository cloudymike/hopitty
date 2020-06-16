import numpy as np
import matplotlib.pyplot as plt
import json
import argparse

def rowprint(row):
    width=6
    s=''
    for x in row:
        s=s+'|{}'.format(str(x)[:width].ljust(width))
    s=s+'|'
    print(s)


parser = argparse.ArgumentParser(description='Read a stages file and create a table')
parser.add_argument('-f', '--file', required=True, help='Input JSON file')
args = parser.parse_args()



with open(args.file) as json_file:
    data = json.load(json_file)


for stage, appliances in data.items():
    collabel = ['stage']
    for appliance, action in appliances.items() :
        collabel.append(appliance)
    break

clust_data = []
for stage, appliances in data.items():
    row = []
    row.append(stage)
    for appliance, action in appliances.items() :
        if action['active']:
            row.append(action['targetValue'])
        else:
            row.append(' ')
    clust_data.append(row)

# Try to display if fail just raw print it
try:
    plt.axis('tight')
    plt.axis('off')
    the_table = plt.table(cellText=clust_data,colLabels=collabel,loc='center')
    plt.show()
except:
    rowprint(collabel)
    for row in clust_data:
        rowprint(row)



