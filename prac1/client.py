# client.py
import socket
import os

# Server configuration
SERVER_IP = input("Enter the server's IP address: ")  # Enter Server's IP address
PORT = 8386  # Server's port

def send_file():
    try:
        # Create a TCP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Attempting to connect to {SERVER_IP}:{PORT}...")
        client_socket.connect((SERVER_IP, PORT))
        print(f"Connected to server at {SERVER_IP}:{PORT}")

        # Get the filename and ensure it exists
        while True:
            filename = input("Enter the full file name (with extension): ")
            if os.path.isfile(filename):  # Ensure the file exists
                break
            print("File not found. Please try again.")

        # Extract just the file name for sending (without the directory path)
        base_filename = os.path.basename(filename)

        # Send the filename to the server
        client_socket.send(base_filename.encode('utf-8') + b'\n')  # Send filename with newline delimiter

        # Open the file and send its content in chunks
        with open(filename, 'rb') as file:
            print(f"Sending file '{base_filename}' to the server...")
            while chunk := file.read(1024):  # Read in chunks of 1KB
                client_socket.send(chunk)

        print(f"File '{base_filename}' sent successfully to the server.")
        client_socket.close()

    except ConnectionRefusedError:
        print("Connection failed: Ensure the server is running and reachable.")
    except socket.timeout:
        print("Connection timed out: Server is taking too long to respond.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    send_file()
