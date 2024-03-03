import socket


class Client:
    
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (self.ip, self.port)
        self.connect()
            
    
    def connect(self):
        try:
            self.client_socket.connect(self.addr)
        except socket.error as e:
            print(str(e))
        
        
    def close(self):
        self.client_socket.close()
        
    
    def send_data(self, data):
        try:
            self.client_socket.send(str.encode(data))
            return(self.client_socket.recv(1024).decode())
        except socket.error as e:
            print(e)
