import socket
import threading
import pickle

HOST = '192.168.0.235'
PORT = 5003
HEADER = 255

DISCONNECT_MESSAGE = '@QUIT'
CHECK_ONLINE_MESSAGE = '@List'

server =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

# a dictionary of online clients including their ids as keys and address as value {id: (addr)}
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

            print(f'{msg}')

            if "Connect" in msg:
                clientId = msg[8:]
                #send interval time for alive message
                conn.send("30".encode())
                send("30", conn)
                connectedClients[clientId] = conn
               
            elif "List" == msg:
                listMessage(conn)

            elif '[MESSAGE]' in msg:
                forwardMessage(clientId, msg)
            
            elif "Quit" == msg:
                connected = quitMessage(msg, clientId)

    conn.close()
    

def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handleClient, args=(conn, addr))
        thread.start()



def quitMessage(msg, clientId):
    connectedClients.pop(clientId)
    return False

    
def listMessage(conn):
    data = pickle.dumps(list(connectedClients.keys()))
    conn.send(data)


def forwardMessage(sourceId, msg):
    parts = msg.split(' ', 2)
    destinationId = parts[1][1:-1]
    writtenMessage = parts[2]

    connectedClients[sourceId].send(writtenMessage.encode())



def updateClientsList():
    pass

def send(msg, conn):
    msg = msg.encode()
    msgLength = len(msg)
    msgLength = str(msgLength).encode()
    msgLength += b' ' * (HEADER - len(msgLength))

    conn.send(msgLength)
    conn.send(msg)




print('[STARTING] Server is starting...')
start()