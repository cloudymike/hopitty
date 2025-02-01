
import pkgutil
import importlib

# This allows to run this as a script, in the "wrong" directory
import sys
sys.path.append('../..')


import sensors

def list_submodules(package_name):
    localClassCollection = {}
    try:
        package = importlib.import_module(package_name)
    except ImportError:
        raise ValueError("Package {} not found".format(package_name))

    if not hasattr(package, '__path__'):
        raise ValueError("{} is not a package".format(package_name))

    submodules = {}
    for _, name, is_pkg in pkgutil.iter_modules(package.__path__):
        full_name = "{}.{}".format(package_name,name)
        try:
            submodule = importlib.import_module(full_name)
            submodules[name]=submodule
            print(name)
            for aName in dir(submodule):
                print("Found", aName)
                aClass = getattr(submodule, aName)
                if hasattr(aClass, "__init__") and \
                    hasattr(aClass, "__module__") and \
                    hasattr(aClass, "getID"):
                    localClassCollection[aName] = aClass
        except ImportError:
            print("Warning: Could not import submodule {}".format(full_name))
    return localClassCollection

class mySensorLoader:
    """
    Finds all sensors and loads them as new objects into a iterable
    dictionary.

    This is a better version that figures out what is a class and then
    just collects those.

    Looks for __init__ and __module__ attribute, and if found assumes
    this is a class
    """

    myClassCollection = {}
    myInstances = {}


    def __init__(self):
        """
        Creates a list of all the classes, as defined in modules in
        package mymods. Modules are defined in __init__.py
        Any class within those modules are collected
        """

        self.myClassCollection=list_submodules('sensors')

    def classes(self):
        return(self.myClassCollection)

    def instances(self):
        return(self.myInstances)

    def build(self):
        """
        This will instantiate one copy of each class found and adding them
        to the myInstances dictionary.
        """
        for className, aClass in self.myClassCollection.iteritems():
            self.myInstances[className] = aClass()

    def list(self):
        """
        This will list all instanticated classes in the myInstances dictionary
        and try one call to them, just for test
        """
        print("============= Listing instantiated classes =============")
        for className, anInstance in self.myInstances.iteritems():
            print('Instance of Class', className, 'has ID', anInstance.getID())


if __name__ == "__main__":
    s = mySensorLoader()
    s.build()
    s.list()
