import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORTS = [5001, 5002, 5003, 5004, 5005]


def process_arithmetic(expression):
    try:
        parts = []
        current_part = ""
        
        for c in expression:
            if c == ' ':
                if current_part != "":
                    parts.append(current_part)
                    current_part = ""
            else:
                current_part += c
        
        if current_part != "":
            parts.append(current_part)
        
        if len(parts) != 3:
            return "Error: Invalid format. Use: add/sub/mul/div num1 num2"
        
        operation = parts[0]
        num1_str = parts[1]
        num2_str = parts[2]
        
        n1 = 0.0
        decimal_place = 0
        found_decimal = False
        for c in num1_str:
            if c == '.':
                found_decimal = True
                continue
            if found_decimal:
                decimal_place += 1
                n1 = n1 + (ord(c) - ord('0')) / (10 ** decimal_place)
            else:
                n1 = n1 * 10 + (ord(c) - ord('0'))
        
        n2 = 0.0
        decimal_place = 0
        found_decimal = False
        for c in num2_str:
            if c == '.':
                found_decimal = True
                continue
            if found_decimal:
                decimal_place += 1
                n2 = n2 + (ord(c) - ord('0')) / (10 ** decimal_place)
            else:
                n2 = n2 * 10 + (ord(c) - ord('0'))
        
        result = 0
        if operation == 'add':
            result = n1 + n2
        elif operation == 'sub':
            result = n1 - n2
        elif operation == 'mul':
            result = n1 * n2
        elif operation == 'div':
            if n2 == 0:
                return "Error: Division by zero"
            result = n1 / n2
        else:
            return "Error: Unknown operation. Use add/sub/mul/div"
        
        return f"Result: {result}"
    except:
        return "Error: Invalid arithmetic expression"


def process_string_analysis(text):
    char_count = 0
    for c in text:
        char_count += 1
    
    word_count = 0
    in_word = False
    for c in text:
        if c == ' ' or c == '\t' or c == '\n':
            if in_word:
                word_count += 1
                in_word = False
        else:
            in_word = True
    if in_word:
        word_count += 1
    
    vowel_count = 0
    for c in text:
        lower_c = c
        if ord(c) >= 65 and ord(c) <= 90:
            lower_c = chr(ord(c) + 32)
        
        if lower_c == 'a' or lower_c == 'e' or lower_c == 'i' or lower_c == 'o' or lower_c == 'u':
            vowel_count += 1
    
    return f"Words: {word_count}, Characters: {char_count}, Vowels: {vowel_count}"


def handle_client(conn, addr, port):
    print(f"[Server {port}] Connected: {addr}")
    
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
                
            message = data.decode("utf-8").strip()
            
            if message.startswith("ARITHMETIC:"):
                expression = message.split(":", 1)[1]
                result = process_arithmetic(expression)
            elif message.startswith("STRING:"):
                text = message.split(":", 1)[1]
                result = process_string_analysis(text)
            else:
                result = "Unknown operation"
            
            timestamp = datetime.now().strftime("%H:%M:%S")
            response = f"[{timestamp}][Server {port}] {result}\n"
            conn.sendall(response.encode("utf-8"))
    
    print(f"[Server {port}] Disconnected: {addr}")


def start_server(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, port))
    s.listen()
    
    print(f"Server listening on port {port}")
    
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr, port), daemon=True).start()


def main():
    print("Starting multiple servers...\n")
    
    for port in PORTS:
        threading.Thread(target=start_server, args=(port,), daemon=True).start()
    
    print(f"\n{len(PORTS)} servers running on ports: {PORTS}")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            threading.Event().wait(1)
    except KeyboardInterrupt:
        print("\nShutting down...")


if __name__ == "__main__":
    main()
