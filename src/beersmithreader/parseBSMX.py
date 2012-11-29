import xml.dom.minidom
import xml.etree.ElementTree as ET


if __name__ == "__main__":
    # Should read in string and remove & 
    doc = xml.dom.minidom.parse("../../beersmith/SilverDollarPorter.bsmx")
    
    
    recipeNameNode = doc.getElementsByTagName("F_R_NAME")
    recipeName = recipeNameNode[0].firstChild.nodeValue
    print "Recipe:", recipeName

    #F_E_NAME
    equipmentNameNode = doc.getElementsByTagName("F_E_NAME")
    equipmentName = equipmentNameNode[0].firstChild.nodeValue
    print "Equipment:", equipmentName
    validEquipment = [
                    'Pot and Cooler ( 5 Gal/19 L) - All Grain'
                    ]
    if equipmentName in validEquipment:
        print "Equipment selected is OK"
    else:
        print "Equipment selected is not available"
    
    
    infuseTempNode = doc.getElementsByTagName("F_MS_INFUSION_TEMP")
    infuseTemp = float(infuseTempNode[0].firstChild.nodeValue)
    print "Infusion temperature:", infuseTemp, "F"
    
    mashTimeNode = doc.getElementsByTagName("F_MS_STEP_TIME")
    mashTime = float(mashTimeNode[0].firstChild.nodeValue)
    print "Mash Time:", mashTime, "min"
    
    infuseVolNode = doc.getElementsByTagName("F_MS_INFUSION")
    infuseVol = float(infuseVolNode[0].firstChild.nodeValue) / 32
    print "Infusion Volume Net:", infuseVol, "qt", infuseVol / 4, "Gallons"
    
    mashTunAdditionNode = doc.getElementsByTagName("F_MS_TUN_ADDITION")
    mashTunAddition = float(mashTunAdditionNode[0].firstChild.nodeValue) / 32
    infuseVolTot = infuseVol + mashTunAddition
    print "Infusion Volume Total:", infuseVolTot, "qt", infuseVolTot / 4, "Gallons"
    
    
    mashMethodNode = doc.getElementsByTagName("F_MH_NAME")
    mashMethod = mashMethodNode[0].firstChild.nodeValue
    print "Mash method:", mashMethod
    validMethods = [
                    'Single Infusion, Light Body, Batch Sparge',
                    'Single Infusion, Medium Body, Batch Sparge',
                    'Single Infusion, Full Body, Batch Sparge'
                    ]
    if mashMethod in validMethods:
        print "Mash Method OK"
    else:
        print "Mash Method not supported"
    
    spargeTempNode = doc.getElementsByTagName("F_MH_SPARGE_TEMP")
    spargeTemp = float(spargeTempNode[0].firstChild.nodeValue)
    print "Sparge Temperature:", spargeTemp
    preboilVolNode = doc.getElementsByTagName("F_E_BOIL_VOL")
    preboilVol = float(preboilVolNode[0].firstChild.nodeValue) / 32
    print "Est Pre-boil volume:", preboilVol, 'qt,', preboilVol/4, 'Gal'
    
    grainWeightNode = doc.getElementsByTagName("F_MS_GRAIN_WEIGHT")
    grainWeight = float(grainWeightNode[0].firstChild.nodeValue) / 16
    print "Grain weight: ", grainWeight, "lb"
    
    grainAbsorption = grainWeight / 8.3 * 4
    print "Grain absorption:", grainAbsorption, "qt", grainAbsorption / 4, "Gallons"
    
    sparge1 = preboilVol / 2 + grainAbsorption - infuseVolTot
    sparge2 = preboilVol / 2
    print "Sparge volume 1:", sparge1, "qt", sparge1 / 4, "Gallons"
    print "Sparge volume 2:", sparge2, "qt", sparge2 / 4, "Gallons"
    
    boilVol1 = infuseVol - grainAbsorption
    boilVol2 = sparge1
    boilVol3 = sparge2
    print "Boiler pump1", boilVol1, "qt", boilVol1 / 4, "Gallons"
    print "Boiler pump1", boilVol2, "qt", boilVol2 / 4, "Gallons"
    print "Boiler pump1", boilVol3, "qt", boilVol3 / 4, "Gallons"
    
    print "Total boil pumped is ", boilVol1 + boilVol2 + boilVol3, "qt", (boilVol1 + boilVol2 + boilVol3) / 4, "Gallons"

    #2.35, 3.72, 6.07
    # F_MS_GRAIN_WEIGHT /16 lb?
    # sparge+infusion vol = pre-boil + grain absorbtion (+/- deadspace)
    # <F_E_NAME>Pot and Cooler ( 5 Gal/19 L) - All Grain</F_E_NAME>
    # Dead space calculation has to be done after 
    # Ditto with temp compensation for equipment
    
    # Alternative that should be easier but did not work
#    tree = ET.parse('../../beersmith/barbary-coast-common-beer.bsmx')

