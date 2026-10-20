import socket
import os
import sys

HOST = "127.0.0.1"

def main():
    # Allow client to choose which server to connect to
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = int(input("Enter server port (5000, 5001, or 5002): "))
    
    pid = os.getpid()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, port))
            print(f"Client PID={pid} connected to Server on port {port}. Type messages:")
            
            while True:
                msg = input("> ")
                if msg.lower() == 'quit':
                    break
                    
                s.sendall((msg + "\n").encode("utf-8"))
                response = s.recv(4096).decode("utf-8", errors="strict")
                print(response, end="")
                
    except ConnectionRefusedError:
        print(f"Error: Could not connect to server on port {port}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
