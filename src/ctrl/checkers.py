

def checkHardware(controllers):
    """
    Checks hardware conditions that should be me
    If any is false return false
    Default is true
    """
    hardwareOK = True

    # Hot water pump and wort pump should not be active at the same time
    if controllers['hotWaterPump'].getPowerOn() and \
    controllers['wortPump'].getPowerOn():
        hardwareOK = False
        print "HotWater pump and wort pump on at same time"

    return(hardwareOK)


def checkRecipe(mycontrollers, recipe, verbose):
    """
    Go through all the stages in the recipe and see
    that the controllers match the controllers available
    """
    for r_key, settings in sorted(recipe.items()):
        print r_key
        if not mycontrollers.check(settings):
            return(False)
    return(True)
