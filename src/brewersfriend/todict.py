import xmltodict

with open('parfait.xml') as fd:
    dict = xmltodict.parse(fd.read())
    
print(dict)