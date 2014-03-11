import xml.dom.minidom
import os
import ctrl
import sys
import mashProfiles
import dataMemcache


class bsmxStages():
    """
    This class will wrap all the bsmx functions. On instantiation, the
    object needs to be passed an xml file and a controller list.
    If the xml file is not a valid recipe, and can not be brewed with the
    controllers, then the validRecipe will be false and any return of
    a stages list will be an empty list.
    """
    def __init__(self, bsmx, controllers):
        self.stages = {}
        self.ctrl = controllers
        self.name = ""
        self.inputTypeDebug = 'NA'

        self.valid = True
        try:
            self.doc = bsmxReadFile(bsmx)
            self.inputTypeDebug = 'file'
        except:
            try:
                self.doc = bsmxReadFromString(bsmx)
                self.inputTypeDebug = 'string'
            except:
                self.doc = bsmx
                try:
                    # Maybe a better check on valid bsmx doc?
                    self.name = bsmxReadName(self.doc)
                    self.valid = self.name != ""
                    self.inputTypeDebug = 'doc'
                except:
                    self.valid = False
                    self.doc = None
                    self.inputTypeDebug = 'NA'

        if self.valid:
            try:
                self.name = bsmxReadName(self.doc)
            except:
                self.valid = False
        if self.valid:
            try:
                self.stages = mashProfiles.txBSMXtoStages(self)
            except:
                self.valid = False

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
        retval = True
        for s_key, stage in self.stages.items():
            for c_key, ctrlType in stage.items():
                if not c_key in self.ctrlList:
                    retval = False
        return(retval)

    def readRecipe(self, data, controllerList):
        pass

    def mkControllerList(self, controllers):
        ctrlLst = []
        for c_key, c in controllers.items():
            ctrlLst.append(c_key)
        return(ctrlLst)

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


##############################################################################
# Old stuff that should be removed at the end.
##############################################################################
def bsmxReadString(doc, tagName):
    recipeStringNode = doc.getElementsByTagName(tagName)
    recipeString = recipeStringNode[0].firstChild.nodeValue
    return(recipeString)


def bsmxReadDispenseOld(doc):
    boiltime = bsmxReadString(doc, "F_E_BOIL_TIME")
    addTimes = []

    print "boiltime", boiltime
    # Find hop additions times
    tagName = "F_H_BOIL_TIME"
    additions = doc.getElementsByTagName(tagName)
    for addItem in additions:
        at = addItem.firstChild.nodeValue
        # if at != boiltime:
        addTimes.append(float(at))

    # Find misc additions times
    tagName = "F_M_TIME"
    additions = doc.getElementsByTagName(tagName)
    for addItem in additions:
        at = addItem.firstChild.nodeValue
        # if at != boiltime:
        addTimes.append(float(at))

    dedupedAddTimes = list(set(addTimes))
    dedupedAddTimes.sort(reverse=True)

    print dedupedAddTimes
    return(dedupedAddTimes)


def bsmxReadTempF(doc, tagName):
    return(float(bsmxReadString(doc, tagName)))


def bsmxReadTimeMin(doc, tagName):
    return(float(bsmxReadString(doc, tagName)))


def bsmxReadVolQt(doc, tagName):
    return(float(bsmxReadString(doc, tagName)) / 32)


def bsmxReadWeightLb(doc, tagName):
    return(float(bsmxReadString(doc, tagName)) / 16)


def setDict(val):
    t = {}
    t['targetValue'] = val
    t['active'] = True
    return(t)


def stageCtrl(controllers):
    settings = {}
    # This is a little clumsy, but during refactoring keep the option of dict
    if isinstance(controllers, dict):
        for c_key, c in controllers.items():
            s = {}
            s['targetValue'] = 0
            s['active'] = False
            settings[c_key] = s
    elif isinstance(controllers, list):
        for c_key in controllers:
            s = {}
            s['targetValue'] = 0
            s['active'] = False
            settings[c_key] = s
    else:
        print "What the heck is controllers?"

    return(settings)


def bsmxReadFromString(bsmxStr):
    bsmxCleanData = bsmxStr.replace('&', 'AMP')
    doc = xml.dom.minidom.parseString(bsmxCleanData)
    return(doc)


def bsmxReadFile(bsmxFile):
    bsmxFD = open(bsmxFile)
    bsmxRawData = bsmxFD.read()
    bsmxFD.close()

    doc = bsmxReadFromString(bsmxRawData)
    return(doc)


def bsmxReadName(doc):
    name = bsmxReadString(doc, "F_R_NAME")
    return(name)


def prettyPrintStages(stages):
    for stage, step in sorted(stages.items()):
        print stage
        for ctrl, val in step.items():
            if val['active']:
                print "    ", ctrl, ":", val['targetValue']


def bsmxReadHops(doc):
    tagName = 'Hops'
    hops = doc.getElementsByTagName(tagName)
    hlist = []
    for hop in hops:
        name = hop.getElementsByTagName("F_H_NAME")[0].firstChild.nodeValue

        boil = hop.getElementsByTagName(
            "F_H_BOIL_TIME")[0].firstChild.nodeValue
        dry = hop.getElementsByTagName(
            "F_H_DRY_HOP_TIME")[0].firstChild.nodeValue
        use = hop.getElementsByTagName("F_H_USE")[0].firstChild.nodeValue
        if use == '0':
            print "Boil", name, boil, "minutes"
            hlist.append(float(boil))
        if use == '1':
            print "Dryhop", name, dry, "days"
    return(hlist)


def returnDispenser(doc, t):
    hlist = bsmxReadDispense(doc)
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


def bsmxHops2Recipe(doc):
    d = dataMemcache.brewData()
    tagName = 'Hops'
    hops = doc.getElementsByTagName(tagName)
    for hop in hops:
        name = hop.getElementsByTagName("F_H_NAME")[0].firstChild.nodeValue
        weight = round(float(hop.getElementsByTagName("F_H_AMOUNT")[0].
                       firstChild.nodeValue), 2)
        boil = hop.getElementsByTagName("F_H_BOIL_TIME")[0].\
            firstChild.nodeValue
        dry = hop.getElementsByTagName("F_H_DRY_HOP_TIME")[0].\
            firstChild.nodeValue
        use = hop.getElementsByTagName("F_H_USE")[0].firstChild.nodeValue
        if use == '0':
            d.addToRecipe(name, weight, returnDispenser(doc, boil))


def bsmxMisc2Recipe(doc):
    d = dataMemcache.brewData()
    tagName = 'Misc'
    misc = doc.getElementsByTagName(tagName)
    for m in misc:
        name = m.getElementsByTagName("F_M_NAME")[0].firstChild.nodeValue

        t = m.getElementsByTagName("F_M_TIME")[0].firstChild.nodeValue
        timeunit = m.getElementsByTagName(
            "F_M_TIME_UNITS")[0].firstChild.nodeValue
        amount = round(float(m.getElementsByTagName(
                       "F_M_AMOUNT")[0].firstChild.nodeValue), 2)
        unit = ""
        use = m.getElementsByTagName("F_M_USE")[0].firstChild.nodeValue
        if timeunit == '0':
            tu = 'minutes'
        if timeunit == '1':
            tu = 'days'

        if use == '0':
            d.addToRecipe(name, amount, returnDispenser(doc, t), unit)


def bsmxGrains2Recipe(doc):
    d = dataMemcache.brewData()
    tagName = 'Grain'
    hops = doc.getElementsByTagName(tagName)
    for hop in hops:
        name = hop.getElementsByTagName("F_G_NAME")[0].firstChild.nodeValue
        weight = round(float(hop.getElementsByTagName("F_G_AMOUNT")[0].
                       firstChild.nodeValue), 2)
        d.addToRecipe(name, weight, 'mashtun')


def bsmxReadMisc(doc):
    tagName = 'Misc'
    ms = doc.getElementsByTagName(tagName)
    mlist = []
    for m in ms:
        name = m.getElementsByTagName("F_M_NAME")[0].firstChild.nodeValue

        t = m.getElementsByTagName("F_M_TIME")[0].firstChild.nodeValue
        unit = m.getElementsByTagName("F_M_TIME_UNITS")[0].firstChild.nodeValue
        use = m.getElementsByTagName("F_M_USE")[0].firstChild.nodeValue
        if unit == '0':
            tu = 'minutes'
        if unit == '0':
            tu = 'days'
        if use == '0':
            print "Boil", name, t, tu
            mlist.append(float(t))
        else:
            print "Other", name, t, tu
    return(mlist)


def bsmxReadDispense(doc):
    addTimes = bsmxReadHops(doc) + bsmxReadMisc(doc)
    dedupedAddTimes = list(set(addTimes))
    dedupedAddTimes.sort(reverse=True)

    print dedupedAddTimes
    return(dedupedAddTimes)


def bsmxRead2DataStore(doc):
    d1 = dataMemcache.brewData()
    d1.clearRecipe()
    bsmxGrains2Recipe(doc)
    bsmxHops2Recipe(doc)
    bsmxMisc2Recipe(doc)
