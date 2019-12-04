#!/usr/bin/env python
 
import socket
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 10062


def writeSocket(command):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.sendall(b'status')
    data = s.recv(1024)
    s.close()
    return(repr(data))



class socketcomm():
    def __init__(self):
        self.BUFFER_SIZE = 20  # Normally 1024, but we want fast response
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))
        # Create a few sockets in case they are not quickly released
        s.listen(10)
        s.setblocking(False)
        self.s = s
        self.conn = None
    
    def getsocket(self):
        return(self.s)
 
    def readSocket(self, status):
        data = ""
        # Assume there is no connecion and check this first.
        
        try:
            fn = self.conn.fileno(), " "
            connected = True
        except:
            try:
                self.conn, addr = self.s.accept()
                self.conn.setblocking(False)
                connected = True
            except:
                connected = False 
                
        
     
        if connected: 
            try:
                data = self.conn.recv(self.BUFFER_SIZE)
                if data:
                    if 'status' in data:
                        self.conn.send(status)  # echo
                    self.conn.close()
            except:
                pass 
    
    
        return(data)


if __name__ == "__main__":
    
    sc = socketcomm()
 
    while 1:
    
        data = sc.readSocket('All OK')
        # This would be the program
        print("Doing stuff with {}".format(data))
        time.sleep(1)
    
    print 'Program ending'
    
