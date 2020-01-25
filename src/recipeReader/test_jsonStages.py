from recipeReader import jsonStages
import os

#========== Start of test code =============


def m2Recipe():
    retDict = {
        "name": "IPA",
        "recipe":  {
            "4step": {
                "wortPump": 1.0
                }
            }
        }
    return(retDict)


def badRecipe():
    retDict = {
        "name": "IPA",
        "recipe":  {
            "4step": {
                "thingimajing": 1.0
                }
            }
        }
    return(retDict)


def ctrlDummyList():
    retlst = ['wortPump', 'boiler']
    return(retlst)


def ctrlDummyDict():
    retlst = {'wortPump': 'dummy1', 'boiler': 'dummy2'}
    return(retlst)


def test_m2Read():
    js = jsonStages(m2Recipe(), ctrlDummyList())
    assert js.getRecipeName() == "IPA"
    stages = js.getStages()
    assert stages["4step"] is not None
    oneStage = stages["4step"]
    assert oneStage is not None
    oneAction = oneStage["wortPump"]
    assert oneAction is not None
    assert oneAction['active']
    assert oneAction['targetValue'] == 1.0
    assert js.isValid()

    print("ok")


def test_m2ReadCtrlDict():
    js = jsonStages(m2Recipe(), ctrlDummyDict())
    assert js.getRecipeName() == "IPA"
    stages = js.getStages()
    assert stages["4step"] is not None
    oneStage = stages["4step"]
    assert oneStage is not None
    oneAction = oneStage["wortPump"]
    assert oneAction is not None
    assert oneAction['active']
    assert oneAction['targetValue'] == 1.0
    assert js.isValid()

    print("ok")


def test_badRecipeRead():
    js = jsonStages(badRecipe(), ctrlDummyList())
    assert js.getRecipeName() == "IPA"
    stages = js.getStages()
    assert stages["4step"] is not None
    oneStage = stages["4step"]
    assert oneStage is not None
    oneAction = oneStage["thingimajing"]
    assert oneAction is not None
    assert oneAction['active']
    assert oneAction['targetValue'] == 1.0
    assert not js.isValid()

    print("ok")


def test_wortpumptest():
    cp = os.path.dirname(__file__)
    print(cp)
    rp = cp + "/../../recipe/wort_pump_test"
    print(rp)
    js = jsonStages(rp, ctrlDummyList())
    print(js.getRecipeName())
    print(js.getStages())
    assert js.getRecipeName() == "wort_pump_test"
    stages = js.getStages()
    assert stages["01"] is not None
    oneStage = stages["01"]
    assert oneStage is not None
    oneAction = oneStage["wortPump"]
    assert oneAction is not None
    assert oneAction['active']
    assert js.isValid()
    print("ok")


if __name__ == "__main__":
    test_m2Read()
    test_wortpumptest()
    test_badRecipeRead()
    test_m2ReadCtrlDict()
