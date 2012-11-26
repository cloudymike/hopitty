import xml.dom.minidom
import xml.etree.ElementTree as ET


if __name__ == "__main__":
    # Should read in string and remove & 
    doc = xml.dom.minidom.parse("../../beersmith/SilverDollarPorter.bsmx")
    infuseTempNode = doc.getElementsByTagName("F_MS_INFUSION_TEMP")
    infuseTemp = float(infuseTempNode[0].firstChild.nodeValue)
    print "Infusion temperature:", infuseTemp, "F"
    
    mashTimeNode = doc.getElementsByTagName("F_MS_STEP_TIME")
    mashTime = float(mashTimeNode[0].firstChild.nodeValue)
    print "Mash Time:", mashTime, "min"
    
    infuseVolNode = doc.getElementsByTagName("F_MS_INFUSION")
    infuseVol = float(infuseVolNode[0].firstChild.nodeValue) / 32
    print "Infusion Volume Net:", infuseVol, "qt"
    
    mashTunAdditionNode = doc.getElementsByTagName("F_MS_TUN_ADDITION")
    mashTunAddition = float(mashTunAdditionNode[0].firstChild.nodeValue) / 32
    infuseVolTot = infuseVol + mashTunAddition
    print "Infusion Volume Total:", infuseVolTot, "qt"
    
    # Dead space calculation has to be done after 
    # Ditto with temp compensation for equipment
    
    # Alternative that should be easier but did not work
#    tree = ET.parse('../../beersmith/barbary-coast-common-beer.bsmx')

