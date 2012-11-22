import appliances.myloader
import ctrl


def testlistbuild():
    l = appliances.myloader.myQuickLoader()
    cll = l.classes().__len__()
    print "Length of class list", cll
    assert cll > 0
    l.build()
    ill = l.instances().__len__()
    print "Length of list", ill
    assert ill > 0
    assert ill == cll


def testget():
    l = appliances.myloader.myQuickLoader()
    l.build()
    for className, instance in l.instances().iteritems():
        x = instance.get()
        assert isinstance(x, int) or isinstance(x, float)


def testloadcontroller():
    c = ctrl.controllerList()
    l = appliances.myloader.myQuickLoader()
    l.build()
    for className, instance in l.instances().iteritems():
        print className
        c.addController(className, instance)
    assert len(c) > 0


def testloadlist():
    c = ctrl.controllerList()
    l = appliances.myloader.myQuickLoader()
    l.build()
    c.addControllerList(l.instances())
    assert len(c) > 0


def testloadself():
    c = ctrl.controllerList()
    c.load()
    assert len(c) > 0
