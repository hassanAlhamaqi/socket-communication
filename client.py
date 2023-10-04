import socket
import time

HOST = '192.168.0.235'
PORT = 5050
HEADER = 255
CLIENT_ID_LENGTH = 8
DISCONNECT_MESSAGE = '@QUIT'



def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    connectMessage(client)

    aliveIntervalTime = client.recv(2048).decode()


"""
    Adds padding to the byte representation of the message length. 
    to ensure that the length of the message is exactly HEADER bytes long. 
    If the length is less than HEADER, spaces are added to fill the remaining space.
"""
def send(msg, client):
    msg = msg.encode()
    msgLength = len(msg)
    msgLength = str(msgLength).encode()
    msgLength += b' ' * (HEADER - len(msgLength))

    client.send(msgLength)
    client.send(msg)



def connectMessage(client):
    clientId = str(input("Enter your client ID: "))

    #if some client has name less than 8 bytes then
    #perform padding to keep it of 8 Bytes

    if len(clientId.encode()) < 8:
        clientId = clientId.ljust(CLIENT_ID_LENGTH, '\0')

    #connect message
    send(f'user {clientId} is connected', client)


def aliveMessage():
    pass


main()