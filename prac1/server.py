# server.py
import socket
import os

# Server configuration
HOST = '172.27.242.41'  # Replace with your server's IP address
PORT = 8386  # Port for communication
SAVE_DIR = "uploaded_files"  # Directory to save received files

def start_server():
    # Ensure the save directory exists
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))  # Bind to the server IP and port
    server_socket.listen(1)  # Allow one client connection at a time
    print(f"Server listening on {HOST}:{PORT}...")

    while True:
        # Accept a connection from a client
        conn, addr = server_socket.accept()
        print(f"Connection established with {addr}")

        try:
            # Receive the filename first, up to the newline character
            filename = b""
            while True:
                byte = conn.recv(1)
                if byte == b'\n':  # Delimiter indicates the end of the filename
                    break
                filename += byte
            filename = filename.decode('utf-8')  # Decode bytes to string
            print(f"Receiving file: {filename}")

            # Define the full path to save the file
            save_path = os.path.join(SAVE_DIR, filename)

            # Open the file to save the incoming data
            with open(save_path, 'wb') as file:
                while True:
                    data = conn.recv(1024)  # Receive file data in chunks (1KB)
                    if not data:  # Condition to check if the file transfer is complete
                        break
                    file.write(data)

            print(f"File '{filename}' received and saved in '{SAVE_DIR}/'.")
        except Exception as e:
            print(f"Error receiving file: {e}")
        finally:
            conn.close()  # Close the client connection
            print(f"Connection with {addr} closed.")

if __name__ == "__main__":
    start_server()
