'''
Created on Mar 19, 2013

@author: mikael
'''


class helloData(object):
    '''
    helloWorld class to test use in both controller and cgi-bin
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.data = "HelloWorld"

    def getData(self):
        return(self.data)
