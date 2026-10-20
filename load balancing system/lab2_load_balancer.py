import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"
LOAD_BALANCER_PORT = 5000
BACKEND_SERVERS = [5001, 5002, 5003]  # Ports for backend servers

# Track active connections for each server
server_loads = {port: 0 for port in BACKEND_SERVERS}


load_lock = threading.Lock()  # Thread-safe access to server_loads


def get_least_loaded_server():
    """Find the server with the least active connections"""
    with load_lock:
        # Find server with minimum load
        least_loaded = min(server_loads.items(), key=lambda x: x[1])
        return least_loaded[0]  # Return port number


def increment_server_load(port):
    """Increment connection count for a server"""
    with load_lock:
        server_loads[port] += 1
        print(f"[Load Balancer] Server {port}: {server_loads[port]} active connections")


def decrement_server_load(port):
    """Decrement connection count for a server"""
    with load_lock:
        server_loads[port] -= 1
        print(f"[Load Balancer] Server {port}: {server_loads[port]} active connections")


def handle_load_balancer_request(conn, addr):
    """Handle client request and assign to least loaded server"""
    try:
        # Receive request from client
        data = conn.recv(1024).decode("utf-8").strip()
        
        # Check if it's a disconnect notification from backend server
        if data.startswith("DISCONNECT:"):
            port = int(data.split(":")[1])
            decrement_server_load(port)
            conn.close()
            return
        
        # Get the least loaded server
        assigned_port = get_least_loaded_server()
        increment_server_load(assigned_port)
        
        # Send assigned port to client
        message = f"ASSIGNED_PORT:{assigned_port}\n"
        conn.sendall(message.encode("utf-8"))
        
        print(f"[Load Balancer] Assigned {addr} to server on port {assigned_port}")
        print(f"[Load Balancer] Current loads: {dict(server_loads)}")
        
    except Exception as e:
        print(f"[Load Balancer] Error handling request from {addr}: {e}")
    finally:
        conn.close()


def run_load_balancer():
    """Main load balancer server"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, LOAD_BALANCER_PORT))
    s.listen()
    
    print(f"[Load Balancer] Listening on {HOST}:{LOAD_BALANCER_PORT}")
    print(f"[Load Balancer] Managing servers on ports: {BACKEND_SERVERS}\n")
    
    while True:
        conn, addr = s.accept()
        # Handle each load balancer request in a separate thread
        threading.Thread(
            target=handle_load_balancer_request,
            args=(conn, addr),
            daemon=True
        ).start()


if __name__ == "__main__":
    run_load_balancer()
