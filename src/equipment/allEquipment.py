import yaml
import glob   

class allEquipment():
    
    def __init__(self, path='src/equipment/*.yaml'):
        files=glob.glob(path)
        self. equipmentlist = {}
        for file in files:
            with open(file) as f:
                equipment = yaml.safe_load(f)
                self.equipmentlist[equipment['equipmentName']] = equipment
                
    def getAll(self):
        return(self.equipmentlist)

    def get(self, equipment):
        if self.exist(equipment):
            return(self.equipmentlist[equipment])
        else:
            return(None)

    def exist(self, equipment):
        return(equipment in self.equipmentlist)
        
if __name__ == '__main__':  # pragma: no cover

    e = allEquipment('./*.yaml')
    #e = allEquipment('grain3g.yaml')
     
    print(e.getAll())
    
    print(e.get('Grain 3G, 5Gcooler, 5Gpot, platechiller'))
    
    if not e.exist('Grain 2.5G, 5Gcooler 4Gpot'):
        print("No such equipment")