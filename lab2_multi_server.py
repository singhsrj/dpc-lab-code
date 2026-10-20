import socket
import threading
from datetime import datetime
import sys

HOST = "127.0.0.1"

def handle_client(conn, addr, server_id):
    # Handle communication with a single client
    print(f"[Server {server_id}] [+] Connected: {addr}")

    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            msg = data.decode("utf-8", errors="ignore").strip()
            print(f"[Server {server_id}] Received: '{msg}' from {addr}")
            reply = (
                f"[{datetime.now().isoformat(timespec='seconds')}] "
                f"Server-{server_id} got '{msg}' from {addr}\n"
            )
            conn.sendall(reply.encode("utf-8"))
        print(f"[Server {server_id}] [-] Disconnected: {addr}")


def run_server(port, server_id):
    # Run a single server instance on the given port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        s.bind((HOST, port))
        s.listen()
        print(f"[Server {server_id}] Listening on {HOST}:{port}")
        
        while True:
            conn, addr = s.accept()
            # Create a new thread for each client
            threading.Thread(
                target=handle_client,
                args=(conn, addr, server_id),
                daemon=True
            ).start()
    except Exception as e:
        print(f"[Server {server_id}] Error: {e}")
    finally:
        s.close()


def main():
    # Start multiple servers on different ports
    ports = [5000, 5001, 5002]  # Define ports for each server
    
    print("Starting multiple servers...")
    
    # Create a thread for each server
    for i, port in enumerate(ports, start=1):
        server_thread = threading.Thread(
            target=run_server,
            args=(port, i),
            daemon=True
        )
        server_thread.start()
    
    print(f"\n{len(ports)} servers are running. Press Ctrl+C to stop.\n")
    
    # Keep main thread alive
    try:
        while True:
            threading.Event().wait(1)
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        sys.exit(0)


if __name__ == "__main__":
    main()
