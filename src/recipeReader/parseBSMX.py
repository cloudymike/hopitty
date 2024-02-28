import xml.dom.minidom
import ctrl
import mashProfiles
import logging
import sys


class bsmxStages():
    """
    This class will wrap all the bsmx functions. On instantiation, the
    object needs to be passed an xml file and a controller list.
    If the xml file is not a valid recipe, and can not be brewed with the
    controllers, then the validRecipe will be false and any return of
    a stages list will be an empty list.
    """
    def __init__(self, bsmx, controllers, recipeonly=False):
        self.stages = {}
        self.ctrl = controllers
        # Start to decouple recipe creation with controller and without
        self.recipeonly = recipeonly
        self.name = ""
        self.inputTypeDebug = 'NA'

        self.valid = True

        try:
            self.docFromFile(bsmx)
            self.inputTypeDebug = 'file'
        except:
            try:
                self.docFromString(bsmx)
                self.inputTypeDebug = 'string'
            except:
                self.doc = bsmx
                try:
                    # Maybe a better check on valid bsmx doc?
                    self.name = bsmxReadString(self.doc, "F_R_NAME")
                    self.valid = self.name != ""
                    self.inputTypeDebug = 'doc'
                except:
                    self.valid = False
                    self.doc = None
                    self.inputTypeDebug = 'NA'


        if self.valid:
            try:
                self.name = bsmxReadString(self.doc, "F_R_NAME")
            except:
                self.valid = False
        if self.valid:
            try:
                self.stages = mashProfiles.txBSMXtoStages(self)
            except:
                self.valid = False
        if self.valid:
            self.valid = self.validateRecipe()


    def __del__(self):
        pass

    def getDocTree(self):
        """
        Returns the doctree, to allow standard dom operations to be applied.
        This should be avoided and instead the built in operations to get
        specific fields should be used.
        """
        return(self.doc)


    def getControllers(self):
        """
        Returns the controller tree, for places where the doc tree is used
        rather than the object.
        This should be avoided and instead the built in operations to get
        specific fields should be used.
        """
        return(self.ctrl)

    def getCtrlEquipmentName(self):
        return(self.ctrl.getEquipmentName())

    def getCtrlEquipment(self):
        return(self.ctrl.getEquipment())

    def getStages(self):
        """
        Returns a valid stages dictionary for the recipe
        """
        return(self.stages)

    def getRecipeName(self):
        return(self.name)

    def isValid(self):
        return(self.valid)

    def validateRecipe(self):
        """
        Simple validation that all appliances in recipe stages
        are also present in the controller.
        """
        if self.ctrl is None:
            return(self.stages is None)
        if self.stages is None:
            return(False)
        retval = True

        for s_key, stage in self.stages.items():
            for c_key, ctrlType in stage.items():
                if not c_key in self.ctrl:
                    retval = False
        return(retval)

    def readRecipe(self, data, controllerList):
        pass

    def mkControllerList(self, controllers):
        ctrlLst = []
        for c_key, c in controllers.items():
            ctrlLst.append(c_key)
        return(ctrlLst)

    def docFromString(self, bsmxStr):
        """
        Creates doc from an xml string
        """
        bsmxCleanData = bsmxStr.replace('&', 'AMP')
        self.doc = xml.dom.minidom.parseString(bsmxCleanData)

    def docFromFile(self, bsmxFile):
        bsmxFD = open(bsmxFile)
        bsmxRawData = bsmxFD.read()
        bsmxFD.close()
        self.docFromString(bsmxRawData)

##############################################################################
# Get fields from key from bsmx file
##############################################################################
    def getFieldStr(self, key):
        """
        Reads a field from xml, and returns the value as a string.
        The field can be anywhere in the doc-tree hierarchy.
        """
        recipeStringNode = self.doc.getElementsByTagName(key)
        recipeString = recipeStringNode[0].firstChild.nodeValue
        return(recipeString)

    def getVolG(self, tagName):
        """Translates a Volume field to gallons, as a float"""
        return(float(self.getFieldStr(tagName)) / 128)

    def getVolQt(self, tagName):
        """Translates a Volume field to quarts, as a float"""
        return(float(self.getFieldStr(tagName)) / 32)

    def getWeightLb(self, tagName):
        """Translates a Weight field to pounds, as a float"""
        return(float(self.getFieldStr(tagName)) / 16)

    def getTempF(self, tagName):
        """Translates a Temperature field to Fahrenheit, as a float"""
        if self.recipeonly:
            return(float(self.getFieldStr(tagName)))
        if tagName == "F_MS_INFUSION_TEMP":
            if self.checkTempAdjust():
                return(float(self.getFieldStr("F_MS_INFUSION_TEMP")))
            else:
                return(self.calcStrikeTemp())
        else:
            return(float(self.getFieldStr(tagName)))

    def getTimeMin(self, tagName):
        """Translates a Time field to minutes, as a float"""
        return(float(self.getFieldStr(tagName)))

##############################################################################
# Start of specific field values. Returns a specific field in right format
##############################################################################
    def getEquipment(self):
        """Return specific BSMX field, name of equipment"""
        return(bsmxReadString(self.doc, "F_E_NAME"))

    def getMashProfile(self):
        """Return specific BSMX field, name of mash profile"""
        return(bsmxReadString(self.doc, "F_MH_NAME"))

    def getGrainAbsorption(self):
        ga = self.getWeightLb("F_MS_GRAIN_WEIGHT") / 8.3 * 4
        return(ga)

    def getTunDeadSpace(self):
        return(self.getVolQt("F_MS_TUN_ADDITION"))

    def getStrikeVolume(self):
        strikeVolNet = self.getVolQt("F_MS_INFUSION")
        strikeVolTot = strikeVolNet + self.getTunDeadSpace()
        return(strikeVolTot)

    def getPreBoilVolume(self):
        return(self.getVolQt("F_E_BOIL_VOL"))

    def getSpargeVolume(self):
        strikeVolNet = self.getVolQt("F_MS_INFUSION")
        return(self.getPreBoilVolume() + self.getGrainAbsorption()
               - strikeVolNet)

    def getDispense(self):
        addTimes = self.getHops() + self.getMisc()

        # Handle just one steep time for now
        steepTimes = self.getSteep()
        if steepTimes:
            logging.debug("Steeping required at time {}".format(steepTimes[0]))
            # Set time to negative to not include in boil time
            addTimes.append(-1 * steepTimes[0])

        dedupedAddTimes = list(set(addTimes))
        dedupedAddTimes.sort(reverse=True)

        logging.debug("Dispenser times: {}".format(str(dedupedAddTimes)))
        return(dedupedAddTimes)

    def getDispenserAtTime(self, t):
        hlist = self.getDispense()
        i = 1
        for h in hlist:
            a = int(float(t))
            b = int(h)
            if a == b:
                dispenser = 'dispenser' + str(i)
                return(dispenser)
            else:
                i = i + 1
        return('error')

    def getSteepTime(self):
        slist = self.getSteep()
        stime = 0
        for s in slist:
            stime = max(stime, s)
        logging.debug("Steep time is:" + str(stime))
        return stime

    def getSteepTemp(self):
        tagName = 'Hops'
        hops = self.doc.getElementsByTagName(tagName)
        steepTemp = 0
        templist = []
        for hop in hops:
            name = hop.getElementsByTagName("F_H_NAME")[0].\
                firstChild.nodeValue
            use = hop.getElementsByTagName("F_H_USE")[0].firstChild.nodeValue
            if use == '4':
                # Beersmith2 does not have a steep temp
                try:
                    steepTstr = hop.getElementsByTagName("F_H_WHIRLPOOL_TEMP")[0].firstChild.nodeValue
                    steepT = float(steepTstr)
                except:
                    steepT = 190
                logging.debug("Steep " + name + " at " + str(steepT) + "F")
                templist.append(float(steepT))
                steepTemp = max(steepTemp, steepT)
        logging.debug("Steep at " + str(steepT) + "F")
        return(steepTemp)


    def getMisc(self):
        tagName = 'Misc'
        ms = self.doc.getElementsByTagName(tagName)
        mlist = []
        for m in ms:
            name = m.getElementsByTagName("F_M_NAME")[0].firstChild.nodeValue

            t = m.getElementsByTagName("F_M_TIME")[0].firstChild.nodeValue
            unit = m.getElementsByTagName("F_M_TIME_UNITS")[0].\
                firstChild.nodeValue
            use = m.getElementsByTagName("F_M_USE")[0].firstChild.nodeValue
            if unit == '0':
                tu = 'minutes'
            if unit == '1':
                tu = 'days'
            if use == '0':
                logging.debug("Boil " + name + " " + str(t) + " " + tu)
                mlist.append(float(t))
            else:
                logging.debug("Other " + name + " " + str(t) + " " + tu)
        return(mlist)

    def getHops(self):
        tagName = 'Hops'
        hops = self.doc.getElementsByTagName(tagName)
        hlist = []
        for hop in hops:
            name = hop.getElementsByTagName("F_H_NAME")[0].\
                firstChild.nodeValue

            boil = hop.getElementsByTagName(
                "F_H_BOIL_TIME")[0].firstChild.nodeValue
            dry = hop.getElementsByTagName(
                "F_H_DRY_HOP_TIME")[0].firstChild.nodeValue
            use = hop.getElementsByTagName("F_H_USE")[0].firstChild.nodeValue
            if use == '0':
                logging.debug("Boil " + name + " " + str(boil) + " minutes")
                hlist.append(float(boil))
            if use == '1':
                logging.debug("Dryhop " + name + " " + str(dry) + " days")
        return(hlist)

    def ingredientsMisc(self):
        tagName = 'Misc'
        ms = self.doc.getElementsByTagName(tagName)
        mlist = []
        for m in ms:
            name = m.getElementsByTagName("F_M_NAME")[0].firstChild.nodeValue

            t = m.getElementsByTagName("F_M_TIME")[0].firstChild.nodeValue
            unit = m.getElementsByTagName("F_M_TIME_UNITS")[0].\
                firstChild.nodeValue
            use = m.getElementsByTagName("F_M_USE")[0].firstChild.nodeValue
            if unit == '0':
                tu = 'minutes'
            if unit == '1':
                tu = 'days'
            if use == '0':
                logging.debug("Boil " + name + " " + str(t) + " " + tu)
                dispenser = self.getDispenserAtTime(float(t))
                try:
                    weight =  m.getElementsByTagName(
                               "F_M_AMOUNT")[0].firstChild.nodeValue
                except:
                    weight = 0
                mlist.append([dispenser, name, weight])
            else:
                logging.debug("Other " + name + " " + str(t) + " " + tu)
        logging.debug("Misc dispenser list: {}".format(mlist))
        return(mlist)

    def ingredientsHops(self):
        tagName = 'Hops'
        hops = self.doc.getElementsByTagName(tagName)
        hlist = []
        for hop in hops:
            name = hop.getElementsByTagName("F_H_NAME")[0].\
                firstChild.nodeValue

            boil = hop.getElementsByTagName(
                "F_H_BOIL_TIME")[0].firstChild.nodeValue
            dry = hop.getElementsByTagName(
                "F_H_DRY_HOP_TIME")[0].firstChild.nodeValue
            use = hop.getElementsByTagName("F_H_USE")[0].firstChild.nodeValue
            if use == '0':
                logging.debug("Boil " + name + " " + str(boil) + " minutes")
                dispenser = self.getDispenserAtTime(float(boil))
                weight =  hop.getElementsByTagName(
                "F_H_AMOUNT")[0].firstChild.nodeValue
                hlist.append([dispenser, name, weight])
            if use == '3':
                weight =  hop.getElementsByTagName(
                "F_H_AMOUNT")[0].firstChild.nodeValue
                hlist.append(['FWH', name, weight])
            if use == '4':
                steep = hop.getElementsByTagName(
                    "F_H_BOIL_TIME")[0].firstChild.nodeValue
                logging.debug("Steep " + name + " " + str(steep) + " minutes")
                #dispenser = self.getDispenserAtTime(float(boil))
                dispenser = self.getDispenserAtTime(-1 * float(steep))
                weight =  hop.getElementsByTagName(
                "F_H_AMOUNT")[0].firstChild.nodeValue
                hlist.append([dispenser, name, weight])
                logging.debug("Steep dispenser:{} name:{} weight:{}, time:{}".format(dispenser,name,weight,boil))
            if use == '1':
                logging.debug("Dryhop " + name + " " + str(dry) + " days")
        logging.debug("Hop dispenser list: {}".format(hlist))
        return(hlist)

    def getSteep(self):
        tagName = 'Hops'
        hops = self.doc.getElementsByTagName(tagName)
        slist = []
        for hop in hops:
            name = hop.getElementsByTagName("F_H_NAME")[0].\
                firstChild.nodeValue

            boil = hop.getElementsByTagName(
                "F_H_BOIL_TIME")[0].firstChild.nodeValue
            dry = hop.getElementsByTagName(
                "F_H_DRY_HOP_TIME")[0].firstChild.nodeValue
            use = hop.getElementsByTagName("F_H_USE")[0].firstChild.nodeValue
            if use == '4':
                logging.debug("Steep " + name + " " + str(boil) + " minutes")
                slist.append(float(boil))
        return(slist)


    def prettyPrintStages(self):
        for stage, step in sorted(self.stages.items()):
            print(stage)
            for ctrl, val in step.items():
                if val['active']:
                    print("    ", ctrl, ":", val['targetValue'])

##############################################################################
# Temperature adjustment methods
##############################################################################
    def checkTempAdjust(self):
        """ Check if temperature adjustment is in place """
        try:
            if  self.getFieldStr('F_MH_EQUIP_ADJUST') != '1':
                return(False)
            else:
                return(True)
        except:
            return(False)

    def getCurrentTemp(self):
        """
        Get environment temp from controller. If not available default to 72F
        """
        try:
            temp = self.ctrl['envTemp'].get()
        except:
            temp = 72
            logging.info("Environment temp not found")
        return(temp)

    def compareStrikeTemp(self):
        """
        Method to compare calculated and Beersmith strike temp. For testing onlyTestMash.onlyTestMash.Method
        TODO The temperature from beersmith grain and tun needs to be extracted
        """
        beersmithTstrike = float(self.getFieldStr("F_MS_INFUSION_TEMP"))
        bsmxGrainTemp = float(self.getFieldStr("F_MH_GRAIN_TEMP"))
        calcTstrike = self.calcStrikeTemp(bsmxGrainTemp)
        logging.debug("beersmith strike T: {}".format(beersmithTstrike))
        logging.debug("calculated strike T: {}".format(calcTstrike))

    def calcStrikeTemp(self, testTemp=None):
        """
        Sets the temperature of the mash in water based on the recipe in
        and the environment temperature, that is applied to both
        grain and equipment
        """
        if testTemp is None:
            envT = self.getCurrentTemp()
        else:
            envT = testTemp
        Mtun = self.getWeightLb('F_E_TUN_MASS')
        Ttun = envT
        Mgrain = self.getWeightLb('F_MH_GRAIN_WEIGHT')
        Tgrain = envT

        Vtun = self.getVolG('F_E_MASH_VOL')
        Qtun = float(self.getFieldStr('F_E_TUN_SPECIFIC_HEAT'))

        Vwater = self.getStrikeVolume()
        Tmash = self.getTempF('F_MS_STEP_TEMP')

        Ffull = 0.39

        Tstrike = (((((Tmash - 32) / 1.8) * (((Mtun / Vtun * Vwater * Ffull)
                    * 453.592 * Qtun) + (Mgrain * 453.592 * 0.38) +
                    (Vwater * 946.353)) -
            ((Mtun / Vtun * Vwater * Ffull) *
                453.592 * Qtun * ((Ttun - 32) / 1.8)) -
            (Mgrain * 453.592 * 0.38 * ((Tgrain - 32) / 1.8))) /
            (Vwater * 946.353)) * 1.8) + 32

        # Use this for validation and testing

        return(Tstrike)

##############################################################################
# Old stuff that should be removed at the end.
##############################################################################
def bsmxReadString(doc, tagName):
    """
    Reads a string from a doc file with tagName tagName.
    In most cases this should not be needed as the above object methods
    should be used, but, for reading a doc file with multiple recipes
    and finding all recipes, it can be useful, as example
    """
    recipeStringNode = doc.getElementsByTagName(tagName)
    recipeString = recipeStringNode[0].firstChild.nodeValue
    return(recipeString)
