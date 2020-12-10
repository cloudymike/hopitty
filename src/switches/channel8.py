import relay_ft245r
import sys
import time
import logging


class oneSwitch():

    def __init__(self, board=None, index=0):
        self.error = False
        self.board = board
        self.index = index
        self.errorStatus = False

    def on(self):
        if self.board is not None:
            try:
                self.board.switchon(self.index)
                self.clearError()
            except:
                self.forceError()

    def off(self):
        if self.board is not None:
            try:
                self.board.switchoff(self.index)
                self.clearError()
            except:
                self.forceError()

    def HWOK(self):
        return (self.board is not None)

    def hasError(self):
        return(self.errorStatus)

    def clearError(self):
        self.errorStatus = False

    def forceError(self):
        self.errorStatus = True


class channel8():  # pragma: no cover
    def __init__(self):

        rb = relay_ft245r.FT245R()
        dev_list = rb.list_dev()

        # list of FT245R devices are returned
        if len(dev_list) == 0:
            logging.error('No FT245R devices found')
            exit(1)

            # Show their serial numbers
        for dev in dev_list:
            logging.info("Found device " + dev.serial_number)

            # Pick the first one for simplicity
        dev = dev_list[0]
        rb.connect(dev)

        logging.info('Using device with serial number ' + str(dev.serial_number))

        self.switchlist = []
        for i in range(0, 9):
            self.switchlist.append(oneSwitch(rb,i))

    def getSwitch(self, index):
        """ yes it is the same as getPump, standard name use """
        return(self.switchlist[index])


if __name__ == "__main__":  # pragma: no cover
    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.INFO,
                        stream=sys.stdout)

    logging.info("Opening channel8 board....")
    ch8 = channel8()
    if ch8.HWOK():
        logging.info("Using HW")
    else:
        logging.info("Just simulating")
        
    for i in range(1, 9):
        currentSwitch = ch8.getSwitch(i)
        logging.info("Toggling switch {}".format(i))
        currentSwitch.on()
        time.sleep(0.5)
        currentSwitch.off()
        time.sleep(1.0)

    logging.info("Done.")
    exit(0)
