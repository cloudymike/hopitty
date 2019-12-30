#!/usr/bin/env python
 
import socket
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 10062

class socketclient():
    
    def __init__(self):
        self.buffersize = 4096

    def write(self, command):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.sendall(command)
        data = s.recv(self.buffersize)
        if len(data) == self.buffersize:
            print("ERROR: buffer overflow")
        s.close()
        return(repr(data))
    


class socketcomm():
    def __init__(self):
        self.BUFFER_SIZE = 32*1024  # Normally 1024, but we want fast response
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))
        # Create a few sockets in case they are not quickly released
        s.listen(10)
        s.setblocking(False)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s = s
        self.conn = None
        
        self.status = ''
    
    def getsocket(self):
        return(self.s)

    def close(self):
        self.s.close()
 
    def read(self, status):
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
                    else:
                        self.conn.send('ok')
                    self.conn.close()
            except:
                pass

        
        return(data)
    
    def set_status(self, status):
        self.status = status
        
    def get_command(self):
        cmd = ''
        data = ''
        command = self.read(self.status)
        if 'terminate' in command:
            cmd='terminate'
        if 'run' in command:
            cmd='run'
        if 'stop' in command:
           cmd='stop'
        if 'pause' in command:
           cmd='pause'
        if '{' in command:
            cmd='loading'
            data = command
        return(cmd, data)

        


if __name__ == "__main__":
    
    sc = socketcomm()
 
    while 1:
    
        data = sc.read('All OK')
        # This would be the program
        print("Doing stuff with {}".format(data))
        time.sleep(1)
    
    print('Program ending')
    
