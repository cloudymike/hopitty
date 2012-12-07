'''
Created on Oct 25, 2012

@author: mikael
'''


class simSwitch(object):
    '''
    Simulated switch. Does not do a lot of things except fullfills the
    required methods of a switch object.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        pass

    def on(self):
        pass

    def off(self):
        pass


# Similar dummy function if a list of switches are required
class simSwitchList():
    def __init__(self):
        pass

    def getSwitch(self, value):
        return(simSwitch())
