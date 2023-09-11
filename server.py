import socket
import sys
import threading
serverPort = int(sys.argv[1])
password = sys.argv[2]
names = []
users = []
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(("localhost", serverPort))
serverSocket.listen(1)
print("Server started on port " + str(serverPort) + ". Accepting connections...")

def receive(connectionSocket):
    try:
        while True:
            searchIndex = 0
            receiverIndex = 0
            for index in range(len(users)):
                if (users[index] == connectionSocket):
                    searchIndex = index
            message = connectionSocket.recv(1024).decode().strip()
            if (message == "exit"):
                print(names[searchIndex] + " left the chatroom")
                for user in users:
                    if(user != connectionSocket):
                        user.send((names[searchIndex] + " left the chatroom" + "\n").encode('utf-8'))
                connectionSocket.close()
                names.remove(names[searchIndex])
                users.remove(connectionSocket)
                break
            elif(":dm" in message):
                dm = ""
                dmchat = message.split(" ")
                receiver = dmchat[1]
                for index in range(len(dmchat)):
                    if (index >= 2):
                        dm += (dmchat[index] + " ")
                for index in range(len(names)):
                    if (names[index] == receiver):
                        receiverIndex = index
                connectionSocket.send((names[searchIndex] + " -> " + names[receiverIndex] + ": " + dm.strip() + "\n").encode('utf-8'))
                users[receiverIndex].send((names[searchIndex] + " -> " + names[receiverIndex] + ": " + dm.strip() + "\n").encode('utf-8'))
                print((names[searchIndex] + " -> " + names[receiverIndex] + ": " + dm.strip()))
            elif(not message):
                print(names[searchIndex] + " left the chatroom")
                connectionSocket.send("error\n".encode('utf-8'))
                for user in users:
                    if(user != connectionSocket):
                        user.send((names[searchIndex] + " left the chatroom" + "\n").encode('utf-8'))
                connectionSocket.close()
                names.remove(names[searchIndex])
                users.remove(connectionSocket)
                break
            else:
                print(names[searchIndex] + ": " + message)
                for user in users:
                    user.send((names[searchIndex] + ": " + message + "\n").encode('utf-8'))
    except:
        print(names[searchIndex] + " left the chatroom")
        connectionSocket.send("error\n".encode('utf-8'))
        for user in users:
            if(user != connectionSocket):
                user.send((names[searchIndex] + " left the chatroom" + "\n").encode('utf-8'))
        connectionSocket.close()
        names.remove(names[searchIndex])
        users.remove(connectionSocket)

def welcome():
    while True:
        connectionSocket, addr = serverSocket.accept()
        messages = connectionSocket.recv(1024).decode().strip().split()
        sentence = messages[0]
        name = messages[1]
        if (sentence == password):
            if (name not in names and " " not in name):
                names.append(name)
                connectionSocket.send(("Welcome!" + "\n").encode('utf-8'))
                for user in users:
                    user.send((name + " joined the chatroom" + "\n").encode('utf-8'))
                print(name + " joined the chatroom")
                users.append(connectionSocket)
                thread3 = threading.Thread(target=receive, args=(connectionSocket,))
                thread3.start()
            else:
                connectionSocket.send(("exit" + "\n").encode('utf-8'))
                connectionSocket.close()
        else:
            connectionSocket.send(("exit" + "\n").encode('utf-8'))
            connectionSocket.close()

thread4 = threading.Thread(target=welcome)
thread4.start()