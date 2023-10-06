import socket
import time
from threading import Thread

HOST = '192.168.0.235'
PORT = 6000
HEADER = 255
CLIENT_ID_LENGTH = 8
DISCONNECT_MESSAGE = '@QUIT'



def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    #send the client id to the server
    clientId = connectMessage(client)

    #alive message
    intervalTime = client.recv(HEADER).decode()
    # print(intervalTime)
    # while True:
    #     aliveMessage(clientId ,client, intervalTime)


    # Create a separate thread for the sleep operation
    sleepThread = Thread(target=aliveMessage, args=(clientId, client, intervalTime))
    sleepThread.daemon = True  # This will allow the program to exit if the main thread exits
    sleepThread.start()

    while True:
        choice = input("""choose or write an action
                    1. @Quit
                    2. @List
                    3  Message to other client
            """)
        if (choice == 1 or choice == '@Quit'):
            send('Quit' ,client)
            break

        elif (choice == 2 or choice == '@List'):
           listMessage()

        elif (choice == 3 or choice == "Message to other client"):
            clientToClientMessage()


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
    clientId = str(input("Enter your ID: "))

    #if some client has name less than 8 bytes then
    #perform padding to keep it of 8 Bytes

    if len(clientId.encode()) <= 8:
        clientId = clientId.ljust(CLIENT_ID_LENGTH, '\0')
    elif len(clientId.encode()) > 8:
        clientId = str(input("Enter your ID: "))

    #connect message
    send(f'Connect {clientId}', client)
    return clientId



def listMessage(client):
        send('List' ,client)
        onlineList = client.recv(HEADER).decode()

def clientToClientMessage():
        otherClientId = input('To send a message to an online client, enter his id:')
        message = input('Enter the message:')   


def aliveMessage(clientId, client, intervalTime):
    while True:
        time.sleep(int(intervalTime))
        send(f'alive {clientId}', client)


main()