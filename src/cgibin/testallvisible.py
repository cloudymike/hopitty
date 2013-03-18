# TODO this is not working
# cgi-bin is not a valid module


import sys
sys.path.append("/home/mikael/workspace/hoppity/src")
sys.path.append("/home/mikael/workspace/hoppity/src/cgi-bin")

import stagesstatus
import start
import recipeliststatus

# Leave this one in and uncomment to validate that
# cgi-bin fails
# The cgi-bin directory will not be picked up by default
# Need link or rename
#def testAllwaysFail():
#    assert False


def teststageStatus():
    stagesstatus.stageStatusMain()


def testStart():
    start.startMain()


def testRecipeListStatus():
    recipeliststatus.recipeliststatusMain()


if __name__ == "__main__":
    teststageStatus()
