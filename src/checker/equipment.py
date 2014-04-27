'''
Created on Apr 12, 2014

@author: mikael
'''

"""
<F_R_EQUIPMENT><_MOD_>1972-05-21</_MOD_>
<F_E_NAME>Grain 3G, 5Gcooler, 5Gpot</F_E_NAME>
<F_E_MASH_VOL>640.0000000</F_E_MASH_VOL>
<F_E_TUN_MASS>160.0000000</F_E_TUN_MASS>
<F_E_BOIL_RATE_FLAG>1</F_E_BOIL_RATE_FLAG>
<F_E_TUN_SPECIFIC_HEAT>0.3000000</F_E_TUN_SPECIFIC_HEAT>
<F_E_TUN_DEADSPACE>64.0000000</F_E_TUN_DEADSPACE>
<F_E_TUN_ADJ_DEADSPACE>1</F_E_TUN_ADJ_DEADSPACE>
<F_E_CALC_BOIL>1</F_E_CALC_BOIL>
<F_E_BOIL_VOL>503.2960000</F_E_BOIL_VOL>
<F_E_BOIL_TIME>60.0000000</F_E_BOIL_TIME>
<F_E_OLD_EVAP_RATE>10.0000000</F_E_OLD_EVAP_RATE>
<F_EQUIP_39>1</F_EQUIP_39>
<F_E_BOIL_OFF>64.0000000</F_E_BOIL_OFF>
<F_E_TRUB_LOSS>38.4000000</F_E_TRUB_LOSS>
<F_E_COOL_PCT>4.0000000</F_E_COOL_PCT>
<F_E_TOP_UP_KETTLE>0.0000000</F_E_TOP_UP_KETTLE>
<F_E_BATCH_VOL>384.0000000</F_E_BATCH_VOL>
<F_E_FERMENTER_LOSS>38.4000000</F_E_FERMENTER_LOSS>
<F_E_TOP_UP>0.0000000</F_E_TOP_UP>
<F_E_EFFICIENCY>58.0000000</F_E_EFFICIENCY>
<F_E_HOP_UTIL>100.0000000</F_E_HOP_UTIL>
<F_E_NOTES></F_E_NOTES>
</F_R_EQUIPMENT>
"""

"""
maxInfusionVol = 18  # quarts, before it goes below heater element
maxTotalInVol = 26  # quarts, before it goes below out spigot
tunDeadSpaceMin = 0.19
boilerVolumeMax = 17
maxTotalWeight = 50 - 5.2 - 1.5 - 1  # 50lb minus mashtun and margin (1lb)
"""

defaultEquipment = {}
defaultEquipment['NAME'] = 'Grain 3G, 5Gcooler, 5Gpot'
defaultEquipment['boilerVolumeMax'] = 17  # Max quarts in boiler
defaultEquipment['maxTotalInVol'] = 26  # quarts, in hw tun
defaultEquipment['maxInfusionVol'] = 18  # quarts, in hw tun above heater


class equipment(object):
    '''
    classdocs
    '''

    def __init__(self,
                 controllers=None,
                 stages=None,
                 ingredients=None,
                 equipmentdata=defaultEquipment):
        '''
        Constructor
        '''
        self.controllers = controllers
        self.stages = stages
        self.ingredients = ingredients
        self.equipmentdata = equipmentdata.copy()

    def updateEquipmentItem(self, equipment, value):
        """
        Update an individual equipments value
        If the equipment does not exist, return false
        This helps finding mistakes by mistyped strings
        """
        if equipment in self.equipmentdata:
            self.equipmentdata[equipment] = value
            return(True)
        else:
            return(False)

    def check(self):
        if not self.__checkRecipeVsController():
            print "Check Fail: RecipeVsController"
            return(False)
        if not self.__checkBoilVolume():
            print "Check Fail: BoilVolume"
            return(False)
        if not self.__checkHotwaterVolume():
            print "Check Fail: HotwaterVolume"
            return(False)
        if not self.__checkHotwaterHeaterVolume():
            print "Check Fail: Hotwater above Heater Volume"
            return(False)
        if not self.__checkBoilerAndWaterHeater():
            print "Check Fail: water Heater and boiler on in same stage"
            return(False)
        if not self.__checkPumpsNoOverlap():
            print "Check Fail: pumps overlapping"
            return(False)
        return(True)

    def __checkRecipeVsController(self):
        """
        Go through all the stages in the recipe and see
        that the controllers match the controllers available
        """
        if self.stages is not None:
            for r_key, settings in sorted(self.stages.items()):
                if not self.controllers.check(settings):
                    return(False)
            return(True)
        return(False)

    def __checkBoilVolume(self):
        totBoilVol = 0.0
        if self.stages is not None:
            for s_key, settings in sorted(self.stages.items()):
                for e_key, e_val in settings.items():
                    if e_key == 'wortPump':
                        totBoilVol = totBoilVol + float(e_val['targetValue'])
        return(totBoilVol <= self.equipmentdata['boilerVolumeMax'])

    def __checkHotwaterVolume(self):
        totHWVol = 0.0
        if self.stages is not None:
            for s_key, settings in sorted(self.stages.items()):
                for e_key, e_val in settings.items():
                    if e_key == 'hotWaterPump':
                        totHWVol = totHWVol + float(e_val['targetValue'])
        if totHWVol > self.equipmentdata['maxTotalInVol']:
            print "Hot water volume:", totHWVol
            return(False)
        else:
            return(True)

    def __checkHotwaterHeaterVolume(self):
        """
        Check that the water heater is not used after water is below
        water heater element.
        """
        totHWVol = 0.0
        if self.stages is not None:
            for s_key, settings in sorted(self.stages.items()):
                for e_key, e_val in settings.items():
                    if e_key == 'hotWaterPump':
                        totHWVol = totHWVol + float(e_val['targetValue'])
                    if (e_key == 'waterHeater') and (e_val['active']):
                        if (totHWVol > self.equipmentdata['maxInfusionVol']):
                            print "Hot water above heater volume:", totHWVol
                            return(False)
        return(True)

    def __checkBoilerAndWaterHeater(self):
        """
        Check that Boiler and WaterHeater is not on in the same step.
        """
        for r_key, settings in sorted(self.stages.items()):
            try:
                waterHeater = int(settings['waterHeater']['targetValue']) != 0
            except:
                waterHeater = False
            try:
                boiler = int(settings['boiler']['targetValue']) != 0
            except:
                boiler = False
            if waterHeater and boiler:
                return(False)
        return(True)

    def __checkPumpsNoOverlap(self):
        """
        Checks hardware conditions that should be met
        If any is false return false
        Default is true
        """
        for r_key, settings in sorted(self.stages.items()):
            try:
                hwp = int(settings['hotWaterPump']['targetValue']) != 0
            except:
                hwp = False
            try:
                wortPump = int(settings['wortPump']['targetValue']) != 0
            except:
                wortPump = False
            try:
                cp = int(settings['circulationPump']['targetValue']) != 0
            except:
                cp = False
            if hwp and wortPump:
                return(False)
            if hwp and cp:
                return(False)
        return(True)
