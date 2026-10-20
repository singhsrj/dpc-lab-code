import socket
import os

HOST = "127.0.0.1"
LOAD_BALANCER_PORT = 5000


def main():
    """Client that connects via load balancer"""
    pid = os.getpid()
    
    print(f"Client PID={pid} requesting server assignment from load balancer...")
    
    # Step 1: Connect to load balancer to get assigned server port
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as lb_socket:
            lb_socket.connect((HOST, LOAD_BALANCER_PORT))
            
            # Send connection request
            lb_socket.sendall(b"REQUEST_SERVER\n")
            
            # Receive assigned port from load balancer
            response = lb_socket.recv(1024).decode("utf-8").strip()
            
            if not response.startswith("ASSIGNED_PORT:"):
                print("Error: Invalid response from load balancer")
                return
            
            assigned_port = int(response.split(":")[1])
            print(f"Load balancer assigned server on port {assigned_port}")
    
    except ConnectionRefusedError:
        print("Error: Load balancer is not running")
        return
    except Exception as e:
        print(f"Error connecting to load balancer: {e}")
        return
    
    # Step 2: Connect to the assigned backend server
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.connect((HOST, assigned_port))
            print(f"Connected to server on port {assigned_port}. Type messages (or 'quit' to exit):\n")
            
            while True:
                msg = input("> ")
                
                if msg.lower() == 'quit':
                    print("Disconnecting...")
                    break
                
                # Send message to server
                server_socket.sendall((msg + "\n").encode("utf-8"))
                
                # Receive response from server
                response = server_socket.recv(4096).decode("utf-8", errors="strict")
                print(response, end="")
                
    except ConnectionRefusedError:
        print(f"Error: Server on port {assigned_port} is not running")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
