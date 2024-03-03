import socket
import threading
import random


class Server:
    
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.gamestate = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.count = random.randint(0, 1)
        
        try:
            self.server_socket.bind((self.ip, self.port))
        except socket.error as e:
            print(str(e))
            
        self.server_socket.listen(2)
        print("Waiting for connection, server started")
        self.accept_thread = threading.Thread(target=self.accept_connections)
        self.accept_thread.start()
    
    
    def close(self):
        self.server_socket.close()
    
        
    def accept_connections(self):
        while True:
            client, address = self.server_socket.accept()
            print("Client connected:", address)
            
            client_thread = threading.Thread(target=self.handle_client, args=(client,))
            client_thread.start()
            
            
    def handle_client(self, client):
        while True:
            try:            
                data = client.recv(1024).decode()
                
                if data == "REQUEST_POSITION":
                    client.send(self.gamestate.encode())
                elif data == "COLOR":
                    position = "white" if self.count % 2 == 1 else "black"
                    client.send(position.encode())
                    self.count += 1
                elif len(data) > 20:
                    self.gamestate = data
                    print("Updated position:", self.gamestate) 
                    client.send(self.gamestate.encode())
            except:
                break
            
        client.close()
