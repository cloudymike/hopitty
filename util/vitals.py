import csv
import argparse
import sys


parser = argparse.ArgumentParser(description='Read a stages file and create a table')
parser.add_argument('-f', '--file', required=True, help='Input JSON file')
args = parser.parse_args()

with open(args.file, 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    isHeader = True
    header = []
    theMatrix = []
    for row in spamreader:
        if isHeader:
            isHeader = False
            for col in row:
                header.append(col)
        else:
            aRow = []
            for col in row:
                aRow.append(col)
            theMatrix.append(aRow)
            
for col in header:
    print('|{}'.format(col)),
print('|')
for row in theMatrix:
    for col in row:
        print('|{}'.format(col)),
    print('|')
        
print('Columns: {}'.format(len(header)))
print('Rows: {}'.format(len(theMatrix)))


