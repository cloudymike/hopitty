#!/usr/bin/env python
 
import socket
import time

def readSocket(s, conn, status):
    data = ""
    # Assume there is no connecion and check this first.
    
    try:
        fn = conn.fileno(), " "
        connected = True
    except:
        try:
            conn, addr = s.accept()
            conn.setblocking(False)
            connected = True
            print "New File number: ", conn.fileno()
        except:
            connected = False 
 
    if connected: 
        try:
            data = conn.recv(BUFFER_SIZE)
            if data:
                if 'status' in data:
                    conn.send(status)  # echo
                conn.close()
        except:
            pass 


    return(conn, data)

if __name__ == "__main__":
 
    TCP_IP = '127.0.0.1'
    TCP_PORT = 10062
    BUFFER_SIZE = 20  # Normally 1024, but we want fast response
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    # Create a few sockets in case they are not quickly released
    s.listen(10)
    print 'Starting loop'
    s.setblocking(False)
    
    
    
    
    
    conn = None
    while 1:
    
        conn, data = readSocket(s,conn,'All OK')
        # This would be the program
        print("Doing stuff with {}".format(data))
        time.sleep(1)
    
    print 'Program ending'
    
