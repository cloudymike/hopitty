import numpy as np
import matplotlib.pyplot as plt
import json

def rowprint(row):
    width=6
    s=''
    for x in row:
        s=s+'|{}'.format(str(x)[:width].ljust(width))
    s=s+'|'
    print(s)

with open('../jsonStages/boiler.golden') as json_file:
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



