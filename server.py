import socket
from threading import Thread
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

PORT = 5000
BUFFER_SIZE = 1024
HOST = "0.0.0.0"
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((HOST, PORT))
server_sock.listen(10)
print("Server online")
print("Host:", HOST + '\n')

clients = []

#Crypto
#Load environment variables from .env file
load_dotenv()
#Get encryption key from environment
KEY = os.getenv("ENCRYPTION_KEY")
if KEY is None:
    raise ValueError("ENCRYPTION_KEY is not set in the environment.")
f = Fernet(KEY)

def handle_client(conn, addr):
    try:
        while True:
            #Recive msg of no more that 1024 bytes
            encrypted_data = conn.recv(BUFFER_SIZE)
            decrypted_data = f.decrypt(encrypted_data)
            decoded_data = decrypted_data.decode()

            if decoded_data == "exit" or not encrypted_data:
                print(f"{addr}: Connection closed")
                #Disconnect client if they send "exit" or send empty data
                break

            print(f"{addr}: {decoded_data}")

            for client in clients:
                if client != conn:
                    #Broadcast data to other clients
                    client.send(f.encrypt(f"{addr}: {decoded_data}".encode()))

    except ConnectionResetError:
        #Catch err in connection
        print(f"{addr}: Connection reset by client")
    finally:
        #Cleanup clients list
        clients.remove(conn)
        conn.close()

if __name__ == "__main__":
    while True:
        #Wait for a cnnection
        conn, addr = server_sock.accept()
        print("Connection:", addr)
        clients.append(conn)
        client_thread = Thread(target=handle_client, args=(conn, addr))
        client_thread.start()
