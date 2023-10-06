import socket
import threading

HOST = '192.168.0.235'
PORT = 6000
HEADER = 255

DISCONNECT_MESSAGE = '@QUIT'
CHECK_ONLINE_MESSAGE = '@List'

server =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

# List to store connected clients
connectedClients = {}

 
def handleClient(conn, addr):

    connected = True
    while connected:

        """
        The client will follow this procedure:
            1. He will send the length of the message in bytes
            2. He will send the actual message
        """
        msg_length = conn.recv(HEADER).decode()
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode()

            if "Connect" in msg:
                clientId = msg[8:]
                #send interval time for alive message
                conn.send("30".encode())
                connectedClients[clientId] = conn
            elif "List" == msg:
                conn.send(connectedClients.encode())
            
            print(f'{msg}')
            connected = checkConnection(msg)

    conn.close()
    connectedClients.remove(conn)

def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handleClient, args=(conn, addr))
        thread.start()



def checkConnection(msg):
    if msg == DISCONNECT_MESSAGE:
        return False
    else:
        return True
    
def getOnlineClients():

    #number of online clients
    onlineClientsNum = len(connectedClients)

    #IDs of online clients
    return connectedClients




print('[STARTING] Server is starting...')
start()