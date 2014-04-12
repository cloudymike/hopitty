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

defaultEquipment = {}


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
        self.equipmentdata = equipmentdata

    def check(self):
        if not self.__checkRecipeVsController():
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
