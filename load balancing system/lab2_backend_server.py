import socket
import threading
from datetime import datetime
import sys

HOST = "127.0.0.1"
LOAD_BALANCER_HOST = "127.0.0.1"
LOAD_BALANCER_PORT = 5000


def handle_client(conn, addr, server_port):
    """Handle communication with a single client"""
    print(f"[Server {server_port}] [+] Client connected: {addr}")
    
    try:
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                
                msg = data.decode("utf-8", errors="ignore").strip()
                print(f"[Server {server_port}] Received: '{msg}' from {addr}")
                
                # Send response back to client
                reply = (
                    f"[{datetime.now().isoformat(timespec='seconds')}] "
                    f"Server-{server_port} processed '{msg}'\n"
                )
                conn.sendall(reply.encode("utf-8"))
                
    except Exception as e:
        print(f"[Server {server_port}] Error with {addr}: {e}")
    finally:
        print(f"[Server {server_port}] [-] Client disconnected: {addr}")
        # Notify load balancer that connection is closed
        notify_load_balancer_disconnect(server_port)


def notify_load_balancer_disconnect(server_port):
    """Notify load balancer that a client disconnected"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((LOAD_BALANCER_HOST, LOAD_BALANCER_PORT))
            # Send disconnect notification
            s.sendall(f"DISCONNECT:{server_port}\n".encode("utf-8"))
    except:
        pass  # Load balancer might be down


def run_backend_server(port):
    """Run a backend server on the specified port"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        s.bind((HOST, port))
        s.listen()
        print(f"[Server {port}] Started and listening on {HOST}:{port}")
        
        while True:
            conn, addr = s.accept()
            # Handle each client in a separate thread
            threading.Thread(
                target=handle_client,
                args=(conn, addr, port),
                daemon=True
            ).start()
            
    except Exception as e:
        print(f"[Server {port}] Error: {e}")
    finally:
        s.close()


def main():
    if len(sys.argv) < 2:
        print("Usage: python lab2_backend_server.py <port>")
        print("Example: python lab2_backend_server.py 5001")
        sys.exit(1)
    
    port = int(sys.argv[1])
    
    print(f"\nStarting backend server on port {port}...")
    print("Press Ctrl+C to stop.\n")
    
    try:
        run_backend_server(port)
    except KeyboardInterrupt:
        print(f"\n[Server {port}] Shutting down...")
        sys.exit(0)


if __name__ == "__main__":
    main()
