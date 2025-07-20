import socket  # noqa: F401


def main():
    # Create a socket that listens on port 4221
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
    # Block until we receive an incoming connection
    connection, address = server_socket.accept()
    # Log the address of the connected client
    print(f"accepted connection from {address}")

    # Read the request from the client
    request = connection.recv(1024).decode()
    
    # Check if the request is a GET request for the root path
    if request.startswith("GET / HTTP/1.1"):
        response = b"HTTP/1.1 200 OK\r\n\r\n"        
    else:
        response = b"HTTP/1.1 404 Not Found\r\n\r\n"

    # Send response to the client
    connection.sendall(response)


if __name__ == "__main__":
    main()
