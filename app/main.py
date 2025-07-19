import socket  # noqa: F401


def main():
    # Create a socket that listens on port 4221
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
    # Block until we receive an incoming connection
    connection, address = server_socket.accept()
    # Log the address of the connected client
    print(f"accepted connection from {address}")
    # Send HTTP 200 OK response to the client
    connection.sendall(b"HTTP/1.1 200 OK\r\n\r\n")


if __name__ == "__main__":
    main()
