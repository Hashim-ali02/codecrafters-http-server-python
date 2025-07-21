import socket  # noqa: F401


def main():
    # Create a socket that listens on port 4221
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
    # Block until we receive an incoming connection
    connection, address = server_socket.accept()
    # Log the address of the connected client
    print(f"accepted connection from {address}")

    # Parse the request from the client
    
    data = connection.recv(1024).decode()
    request = data.split("\r\n")[0]
    method, path, version = request.split(" ")

    # Check if method, path, and version are valid
    if method == "GET" and path == "/" and version == "HTTP/1.1": 
        response = "HTTP/1.1 200 OK\r\n\r\n"
    elif method == "GET" and path.startswith("/echo/"):
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(request[6:])}\r\n\r\n{request[6:]}"        
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"

    # Send response to the client
    connection.sendall(response.encode())


if __name__ == "__main__":
    main()
