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
    
# Find the value if the check is GT 0 for the first time
def valueIfGT0(theMatrix, header, checkLabel, valueLabel):
    for row in theMatrix:
        if float(row[header.index(checkLabel)]) > 0:
            return(row[header.index(valueLabel)])

# Find the value if the check is GT 0 for the first time
def valueIf0(theMatrix, header, checkLabel, valueLabel):
    nonZerosFound = False
    for row in theMatrix:
        # Skip any initial 0
        if float(row[header.index(checkLabel)]) > 0:
            nonZerosFound = True
        if nonZerosFound and row[header.index(checkLabel)] == '0':
            return(row[header.index(valueLabel)])

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
            # TODO, some initial rows are not initialized, multithread issue? Check on hwt that should have a number.
            if row[header.index('waterHeater')] != '0':
                theMatrix.append(aRow)
            

#print('Columns: {}'.format(len(header)))
#print('Rows: {}'.format(len(theMatrix)))

print('Env temp: {}'.format(valueIfGT0(theMatrix, header, 'envTemp', 'envTemp')))
print('Strike water temp: {}'.format(valueIfGT0(theMatrix, header, 'hotWaterPump', 'waterHeater')))
print('Sparge water temp: {}'.format(valueIfGT0(theMatrix, header, 'wortPump', 'waterHeater')))

try:
    print('Initial mash temp: {}'.format(valueIf0(theMatrix, header, 'hotWaterPump', 'mashTemp')))
    print('Final mash temp: {}'.format(valueIfGT0(theMatrix, header, 'wortPump', 'mashTemp')))
    print('Max mash temp: {}'.format(max(column(theMatrix, header.index('mashTemp')))))
except:
    print('Mash temp missing')

try:
    hwtFull = float(max(column(theMatrix,header.index('hwtVolume'))))
    hwtEmpty = float(min(column(theMatrix,header.index('hwtVolume'))))
    strikeVol = hwtFull - float(valueIfGT0(theMatrix, header, 'wortPump', 'hwtVolume'))
    spargeVol = hwtFull - hwtEmpty - strikeVol
    print('Strike water volume: {}'.format(strikeVol))
    print('Sparge water volume: {}'.format(spargeVol))
    print('Boil volume: {}'.format(max(column(theMatrix,header.index('boilerVolume')))))
except:
    print('Volume info missing')

# Verbose debugging stuff    
#reprintCsv(header, theMatrix)
#print(column(theMatrix,header.index('mashTemp')))
#print(theMatrix[0])

