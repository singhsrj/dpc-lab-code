import socket
import threading
import time

node_name = ""
server_port = 0
peer_host = ""
peer_port = 0
local_client_conn = None
peer_server_conn = None

def start_server():
    global local_client_conn, peer_server_conn
    
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('0.0.0.0', server_port))
    server_sock.listen(2)
    print(f"{node_name} Server listening on port {server_port}")
    
    conn1, addr1 = server_sock.accept()
    conn2, addr2 = server_sock.accept()
    
    if addr1[1] > 49152:
        local_client_conn = conn1
        peer_server_conn = conn2
    else:
        local_client_conn = conn2
        peer_server_conn = conn1
    
    threading.Thread(target=forward_messages, daemon=True).start()
    receive_messages()

def forward_messages():
    while True:
        try:
            msg = local_client_conn.recv(1024)
            if msg:
                peer_server_conn.send(msg)
        except:
            break

def receive_messages():
    while True:
        try:
            msg = peer_server_conn.recv(1024).decode('utf-8')
            if msg:
                print(f"\n{node_name} Received: {msg}")
                print(f"{node_name} You: ", end='', flush=True)
        except:
            break

def connect_to_peer():
    time.sleep(2)
    while True:
        try:
            peer_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_sock.connect((peer_host, peer_port))
            break
        except:
            pass

def send_messages():
    time.sleep(1)
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('127.0.0.1', server_port))
    
    while True:
        msg = input(f"{node_name} You: ")
        client_sock.send(msg.encode('utf-8'))

node_name = input("Enter Node name: ")
server_port = int(input(f"Enter {node_name}'s port: "))
peer_port = int(input("Enter peer port: "))
peer_host = "127.0.0.1"

threading.Thread(target=start_server, daemon=True).start()
threading.Thread(target=connect_to_peer, daemon=True).start()

time.sleep(1)

send_messages()
