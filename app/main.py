import socket 
import threading
import sys

def main():
    start_server()
    
def get_file_contents(path):
    file_path = sys.argv[2] + path
    try:
        with open(file_path) as file:
            return file.read()
    except:
        return False

def start_server():    
    # Create a socket that listens on port 4221
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        connection, address = server_socket.accept()  
        thread = threading.Thread(target=handleconnection, args=(connection, address))
        thread.start()

        
def handleconnection(connection, address):      
    # Parse the request from the client
    data = connection.recv(2048).decode()
    split_data = data.split("\r\n")
    request = split_data[0]
    host = split_data[1]
    user_agent = split_data[2]
    method, path, version = request.split(" ")

    # Check if method, path, and version are valid
    if method == "GET" and path == "/" and version == "HTTP/1.1": 
        response = "HTTP/1.1 200 OK\r\n\r\n"
    elif method == "GET" and path.startswith("/echo/"):
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(path[6:])}\r\n\r\n{path[6:]}"
    elif method == "GET" and path == "/user-agent":
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent[12:])}\r\n\r\n{user_agent[12:]}"        
    elif path.startswith("/files/") and get_file_contents(path[7:]) != False:
        content = get_file_contents(path[7:])
        response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(content)}\r\n\r\n{content}"
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"

    # Send response to the client
    connection.sendall(response.encode())


if __name__ == "__main__":
    main()
