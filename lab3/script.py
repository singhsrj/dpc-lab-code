import socket
import threading
import time

peer_connection = None
node_name = ""
server_port = 0
peer_host = ""
peer_port = 0

def start_server():
    global peer_connection

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server.bind(('0.0.0.0', server_port))
    
    server.listen(1)
    print(f"{node_name} Server listening on port {server_port}")
    
    conn, addr = server.accept()
    print(f"{node_name} Connected to peer at {addr}")
    peer_connection = conn
    
    receive_messages()

def connect_to_peer():
    global peer_connection
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((peer_host, peer_port))
    
            peer_connection = client
            print(f"{node_name} Connected to peer server at {peer_host}:{peer_port}")
            receive_messages()
            break
        except:
            pass

def receive_messages():
    while True:
        try:
            message = peer_connection.recv(1024).decode('utf-8')
            if message:
                print(f"\n{node_name} Received: {message}")
                print(f"{node_name} You: ", end='', flush=True)
            else:
                break
        except:
            break

def send_messages():
    while True:
        message = input(f"{node_name} You: ")
        if peer_connection:
            try:
                peer_connection.send(message.encode('utf-8'))
            except:
                print(f"{node_name} Failed to send message")

node_name = input("Enter Node name: ")
server_port = int(input(f"Enter {node_name}'s port: "))
peer_port = int(input("Enter peer port: "))
peer_host = "127.0.0.1"

threading.Thread(target=start_server, daemon=True).start()
threading.Thread(target=connect_to_peer, daemon=True).start()

time.sleep(1)

send_messages()


