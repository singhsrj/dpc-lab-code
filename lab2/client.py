import socket
import random

HOST = "127.0.0.1"
PORTS = [5001, 5002, 5003, 5004, 5005]


def main():
    port = random.choice(PORTS)
    
    print("Select operation type:")
    print("1. Arithmetic Processing")
    print("2. String Analysis")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice not in ['1', '2']:
        print("Invalid choice")
        return
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, port))
            print(f"\nConnected to server on port {port}\n")
            
            while True:
                if choice == '1':
                    data = input("Enter arithmetic expression (or 'quit'): ")
                    if data.lower() == 'quit':
                        break
                    message = f"ARITHMETIC:{data}"
                else:
                    data = input("Enter text for analysis (or 'quit'): ")
                    if data.lower() == 'quit':
                        break
                    message = f"STRING:{data}"
                
                s.sendall(message.encode("utf-8"))
                response = s.recv(4096).decode("utf-8")
                print(response)
                
    except ConnectionRefusedError:
        print(f"Error: Could not connect to server on port {port}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
