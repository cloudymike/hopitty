'''
Created on Oct 25, 2012

@author: mikael
'''
import serial
import time
import getopt
import sys
from struct import *
import logging

SERIAL_PATH = '/dev/serial/by-id/usb-Devantech_Ltd._USB-RLY02._00019896-if00'
BAUD_RATE = 9600

commands = {
    'relay_1_on': 0x6F,
    'relay_1_off': 0x65,
    'relay_2_on': 0x66,
    'relay_2_off': 0x70,
    'info': 0x5A,
    'relay_states': 0x5B,
}


def send_command(cmd, read_response=False):
    try:
        ser = serial.Serial(SERIAL_PATH, BAUD_RATE)
        ser.write(chr(cmd) + '\n')
        response = read_response and ser.read() or None
        ser.close()
    except:
        print("ERROR, can not connect to powerswitch")
        response = None
    return response


def get_relay_states():
    states = send_command(commands['relay_states'], read_response=True)
    response = unpack('b', states)[0]
    states = {
        0: {'1': False, '2': False},
        1: {'1': True, '2': False},
        2: {'1': False, '2': True},
        3: {'1': True, '2': True},
    }
    return states[response]


class powerSwitch(object):
    '''
    Simulated switch. Does not do a lot of things except fullfills the
    required methods of a switch object.
    '''

    def __init__(self, relay=1):
        '''
        Constructor
        '''
        self.relay = relay
        self.simulation = False

        try:
            relaystates = get_relay_states()
        except:
            self.simulation = True

    def on(self):
        #print "Power switch " + str(self.relay) + " on"
        if self.simulation:
            pass
        else:
            if self.relay == 1:
                send_command(commands['relay_1_on'])
            if self.relay == 2:
                send_command(commands['relay_2_on'])

    def off(self):
        #print "Power switch " + str(self.relay) + " off"
        if self.simulation:
            pass
        else:
            if self.relay == 1:
                send_command(commands['relay_1_off'])
            if self.relay == 2:
                send_command(commands['relay_2_off'])

    def HWOK(self):
        return(not self.simulation)

if __name__ == '__main__':  # pragma: no cover
    testHWtun = powerSwitch(1)
    testBoiler = powerSwitch(2)

    hwok = testHWtun.HWOK()
    if hwok:
        print("Hardware switch found with HWOK method")
    else:
        print("Hardware switch not found with HWOK method")

    for i in range(1, 10):
        print("HWtun on")
        testHWtun.on()
        time.sleep(1)
        print("HWtun off")
        testHWtun.off()

        time.sleep(1)
        print("Boiler on")
        testBoiler.on()
        time.sleep(1)
        print("Boiler off")
        testBoiler.off()
        time.sleep(1)
