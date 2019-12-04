import netsock
import time

if __name__ == "__main__":
    
    sc = netsock.socketcomm()
 
    while 1:
    
        data = sc.readSocket('All OK')
        # This would be the program
        print("Doing stuff with {}".format(data))
        time.sleep(1)
    
    print('Program ending')
