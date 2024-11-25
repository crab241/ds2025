# server.py
import socket

# Server configuration
HOST = '172.23.189.121'  # Replace with your server's IP address
PORT = 8386  # Port for communication

def start_server():
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))  # Bind to the server IP and port
    server_socket.listen(1)  # Allow one client connection at a time
    print(f"Server listening on {HOST}:{PORT}...")

    while True:
        # Accept a connection from a client
        conn, addr = server_socket.accept()
        print(f"Connection established with {addr}")

        # Receive the filename first, up to the newline character
        filename = b""
        while True:
            byte = conn.recv(1)
            if byte == b'\n':  # Delimiter indicates the end of the filename
                break
            filename += byte
        filename = filename.decode('utf-8')  # Decode bytes to string
        print(f"Receiving file: {filename}")

        # Open the file with the received filename to save the incoming data
        with open(filename, 'wb') as file:
            while True:
                data = conn.recv(1024)  # Receive file data in chunks (1KB)
                if not data:  # No more data means the file transfer is complete
                    break
                file.write(data)

        print(f"File '{filename}' received and saved in the server folder.")
        conn.close()  # Close the client connection
        print(f"Connection with {addr} closed.")

if __name__ == "__main__":
    start_server()
