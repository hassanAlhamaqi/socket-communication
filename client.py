import socket
import time
import pickle
from threading import Thread

HOST = '192.168.0.235'
PORT = 5003
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
        if (choice == '1' or choice == '@Quit'):
            send('Quit' ,client)
            client.close()
            break

        elif (choice == '2' or choice == '@List'):
           listMessage(client)
           

        elif (choice == '3' or choice == "Message to other client"):
            clientToClientMessage(client)


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
        onlineList = client.recv(HEADER)
        onlinelist = pickle.loads(onlineList)  # Deserialize the data using pickle

        onlineUsersNum = len(onlinelist)

        # print(f'Their are {len(data)} online clients:')
        print(f'Their are {onlineUsersNum} online clients:' if onlineUsersNum > 1 else f'Their is {onlineUsersNum} online client:')
        for clientId in onlinelist:
            print(f'clientId: {clientId}')



def clientToClientMessage(client):
        otherClientId = input('To send a message to an online client, enter his id:')
        msg = input('Enter the message:')
        send(f'[MESSAGE] ({otherClientId}) {msg}', client)


def aliveMessage(clientId, client, intervalTime):
    while True:
        time.sleep(int(intervalTime))
        send(f'alive {clientId}', client)


main()