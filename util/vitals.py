import csv
import argparse
import sys


parser = argparse.ArgumentParser(description='Read a stages file and create a table')
parser.add_argument('-f', '--file', required=True, help='Input JSON file')
args = parser.parse_args()

def reprintCsv(headers, theMatrix):
    for col in header:
        print('|{}'.format(col)),
    print('|')
    for row in theMatrix:
        for col in row:
            print('|{}'.format(col)),
        print('|')

def column(theMatrix, colindex):
    col = []
    for row in theMatrix:
        col.append(row[colindex])
    return(col)

with open(args.file, 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    isHeader = True
    theMatrix = []
    for row in csvreader:
        if isHeader:
            header = []
            isHeader = False
            for col in row:
                header.append(col)
        else:
            aRow = []
            for col in row:
                aRow.append(col)
            theMatrix.append(aRow)
            

print('Columns: {}'.format(len(header)))
print('Rows: {}'.format(len(theMatrix)))
print('Index of Time: {}'.format(header.index('Time')))
print('Index of cooler: {}'.format(header.index('cooler')))
print('Index of boilerVolume: {}'.format(header.index('boilerVolume')))
print('Max boilerVolume: {}'.format(max(column(theMatrix,header.index('boilerVolume')))))

reprintCsv(header, theMatrix)

