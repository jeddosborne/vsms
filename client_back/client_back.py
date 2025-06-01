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
#Enable nodelay for faster transmition (less bandwidth efficient)
#client_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
BUFFER_SIZE = 1024
#SERVER_HOST = input("Server hostname: ") #User chooses server by IP
#SERVER_HOST = "86.145.213.203" #Server public IP
SERVER_HOST = "localhost" #For testing
SERVER_PORT = 5000 #86.145.213.203:5000 port forwaded to my laptop's port 5000

exited = False
all_msgs = []

user_prefs = {
    "theme": "system",
    "tint": "blue"
}

client_sock.connect((SERVER_HOST, SERVER_PORT))
print("Connected to server")
all_msgs.append("Connected to server")
all_msgs.append("Use '//exit' to close connection\n")
all_msgs.append("Your first message will be your display name:")

def send_msg(client_sock, msg):
    global exited
    encrypted_msg = f.encrypt(msg.encode())
    
    if msg == "//exit":
        client_sock.close()
        print("Connection closed")
        all_msgs.append("Connection closed")
        exited = True
    else:
        if msg[:2] == "//":
            all_msgs.append(f"CMD: {msg}\n")
            if len(msg.split()) != 2:
                all_msgs.append("Commands must have one parameter\n")
            else:
                command = msg.split()[0]
                param = msg.split()[1]
                match command:
                    case "//theme":
                        if param in ["system", "dark", "light"]:
                            user_prefs["theme"] = param
                        else:
                            all_msgs.append(f"Invalid parameter: {param}\n")
                    case "//tint":
                        if param in ["blue", "green"]:
                            user_prefs["tint"] = param

                        else:
                            all_msgs.append(f"Invalid parameter: {param}\n")
                    case _:
                        all_msgs.append(f"Invalid command: {command}\n")

        else:
            client_sock.send(encrypted_msg)
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
