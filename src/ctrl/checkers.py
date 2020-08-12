import sys


def checkHardware(controllers):
    """
    Checks hardware conditions that should be met
    If any is false return false
    Default is true
    """
    hardwareOK = True

    # Hot water pump and wort pump should not be active at the same time
    if controllers['hotWaterPump'].getPowerOn() and \
            controllers['wortPump'].getPowerOn():
        hardwareOK = False
        print("HotWater pump and wort pump on at same time")

# 130916 removed mashCirculationPump
#    if controllers['mashCirculationPump'].getPowerOn() and \
#    controllers['wortPump'].getPowerOn():
#        hardwareOK = False
#        print("Mash circulation pump and wort pump on at same time")

    if controllers['hotWaterPump'].getPowerOn() and \
            controllers['waterCirculationPump'].getPowerOn():
        hardwareOK = False
        print("HotWater pump and Hot Water circulation pump on at same time")

    return(hardwareOK)


def checkRecipe(mycontrollers, recipe, verbose):
    if checkRecipeVsController(mycontrollers, recipe, verbose):
        print("Recipe OK")
        if checkBoilerAndWaterHeater(mycontrollers, recipe, verbose):
            return(True)
    print("checkRecipe failed")
    return(False)


def checkRecipeVsController(mycontrollers, recipe, verbose):
    """
    Go through all the stages in the recipe and see
    that the controllers match the controllers available
    """
    if recipe is not None:
        for r_key, settings in sorted(recipe.items()):
            if verbose:
                print(r_key)
            if not mycontrollers.check(settings):
                return(False)
        return(True)
    return(False)


def checkBoilerAndWaterHeater(mycontrollers, recipe, verbose):
    """
    Check that Boiler and WaterHeater is not on in the same step.
    """
    for r_key, settings in sorted(recipe.items()):
        try:
            waterHeater = int(settings['waterHeater']['targetValue']) != 0
        except:
            waterHeater = False
        try:
            boiler = int(settings['boiler']['targetValue']) != 0
        except:
            boiler = False
        if waterHeater and boiler:
            print("Error: water Heater and boiler on in stage", r_key)
            return(False)
    return(True)
