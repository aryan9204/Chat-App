import socket
import sys
import threading
from datetime import datetime
import os
serverName = sys.argv[1]
port = int(sys.argv[2])
password = sys.argv[3]
name = sys.argv[4]
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, port))
print("Connecting to " + serverName + " on port " + str(port) + "...")
clientSocket.send((password + "\n").encode('utf-8'))
clientSocket.send((name + "\n").encode('utf-8'))
welcome = clientSocket.recv(1024).decode().strip()
if (welcome == "exit"):
    clientSocket.close()
    os._exit(1)
else:
    print(welcome)

def receive():
    while True:
        try:
            message = clientSocket.recv(1024).decode().strip()
            if (message == "error"):
                clientSocket.close()
                os._exit(1)
            print(message)
        except:
            clientSocket.close()
            os._exit(1)
def send():
    while True:
        chat = input()
        if(chat == ":Exit"):
            clientSocket.send(("exit" + "\n").encode('utf-8'))
            clientSocket.close()
            os._exit(0)
        elif(chat == ":)"):
            clientSocket.send(("[feeling happy]"+"\n").encode('utf-8'))
        elif(chat == ":("):
            clientSocket.send(("[feeling sad]"+"\n").encode('utf-8'))
        elif(chat == ":mytime"):
            time = datetime.now()
            clientSocket.send((f"It's {time.strftime('%H')}:{time.strftime('%M')} on {time.strftime('%a')}, {time.strftime('%d')} {time.strftime('%b')}, {time.strftime('%Y')}.\n").encode('utf-8'))
        elif(chat == ":dm"):
            clientSocket.send((chat + "\n").encode('utf-8'))
        else:
            clientSocket.send((chat + "\n").encode('utf-8'))       
 


thread1 = threading.Thread(target=receive)
thread1.start()

thread2 = threading.Thread(target=send)
thread2.start()