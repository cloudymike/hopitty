# Testing:
#   That the runstage works
#   That skip works
#
import dataMemcache
import ctrl
import datetime


def testStart():
    mydata = dataMemcache.brewData()
    ru = ctrl.rununit()
    clist = ru.getControllers()

    stages = {}
    s1 = ctrl.stageCtrl(clist)
    s1["delayTimer"] = ctrl.setDict(1)
    stages["1"] = s1

    s2 = ctrl.stageCtrl(clist)
    s2["delayTimer"] = ctrl.setDict(0.03)
    stages["2"] = s2
    ru.stagesIn(stages)

    mydata.setRunStatus('run')
    mydata.setSkip(True)
    startTime = datetime.datetime.now()
    ru.runStage('1', stages['1'])
    delta = datetime.datetime.now() - startTime
    deltasec = delta.total_seconds()
    print delta, deltasec
    assert deltasec < 1.0

    mydata.setSkip(False)
    startTime = datetime.datetime.now()
    ru.runStage('2', stages['2'])
    delta = datetime.datetime.now() - startTime
    deltasec = delta.total_seconds()
    print delta, deltasec
    assert deltasec > 1.0

    print "OK"

if __name__ == "__main__":
    testStart()