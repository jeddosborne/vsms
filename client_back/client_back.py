import socket
from threading import Thread
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

#Crypto
#Load environment variables from .env file
load_dotenv()
#Get encryption key from environment
KEY = os.getenv("ENCRYPTION_KEY")
if KEY is None:
    raise ValueError("ENCRYPTION_KEY is not set in the environment.")
f = Fernet(KEY)

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Enable nodelay for faster transmition
client_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
BUFFER_SIZE = 1024
#SERVER_HOST = input("Server hostname: ")
SERVER_HOST = "86.145.213.203" #Server public IP
SERVER_PORT = 5000 #86.145.213.203:5000 port forwaded to my laptop's port 5000

exited = False
all_msgs = []

client_sock.connect((SERVER_HOST, SERVER_PORT))
print("Connected to server")
all_msgs.append("Connected to server")
all_msgs.append("Use 'exit' to close connection")
all_msgs.append("Your first message will be your display name\n")

def send_msg(client_sock, msg):
    global exited
    encrypted_msg = f.encrypt(msg.encode())
    #Send inputted msg
    client_sock.send(encrypted_msg)
    if msg == "exit":
        client_sock.close()
        print("Connection closed")
        all_msgs.append("Connection closed")
        exited = True
    else:
        all_msgs.append(f"You: {msg}\n")

        

def recv_data(client_sock):
    while True:
        #Recieve msg of no more that 1024 bytes
        data = client_sock.recv(BUFFER_SIZE)
        if not data:
            print("Connection broken")
            all_msgs.append("Connection broken")
            break
        decrypted_data = f.decrypt(data)
        decoded_data = decrypted_data.decode()
        print(decoded_data)
        all_msgs.append(f"{decoded_data}\n")

#Thread to recieve messages
recv_thread = Thread(target=recv_data, args=(client_sock,))
recv_thread.start()
