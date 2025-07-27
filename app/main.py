import socket 
import threading
import sys
import gzip

def main():
    start_server()
    
def get_file_contents(path):
    file_path = sys.argv[2] + path
    try:
        with open(file_path) as file:
            return file.read()
    except:
        return False

def create_file(path, content):
    file_path = sys.argv[2] + path
    try:
        with open(file_path, "w") as file:
            file.write(content)
        return True
    except:
        return False

def start_server():    
    # Create a socket that listens on port 4221
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        connection, address = server_socket.accept()  
        thread = threading.Thread(target=handleconnection, args=(connection, address))
        thread.start()

def encoded_response(encodings, body):
    acceptable_encodings = ["gzip"]
    for encoding in encodings:
        if encoding in acceptable_encodings:
            compressed_body = compress_body(encoding, body)
            headers = f"HTTP/1.1 200 OK\r\nContent-Encoding: {encoding}\r\nContent-Type: text/plain\r\nContent-Length: {len(compressed_body)}\r\n\r\n"
            return headers.encode() + compressed_body
    return f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n"
        
def compress_body(encoding, body):
    if encoding == "gzip":
        return gzip.compress(body.encode())
    else:
        return body
    

def handleconnection(connection, address):      
    # Parse the request from the client
    data = connection.recv(2048).decode()
    request_data, body = data.split("\r\n\r\n")
    request = request_data.split("\r\n")[0]
    headers = request_data.split("\r\n")[1:]
    method, path, version = request.split(" ")

    parsed_headers = {}
    for header in headers:
        key, value = header.split(": ")
        parsed_headers[key] = value

    # Check if method, path, and version are valid
    if method == "GET" and path == "/" and version == "HTTP/1.1": 
        response = "HTTP/1.1 200 OK\r\n\r\n"
    elif method == "GET" and "Accept-Encoding" in parsed_headers and path.startswith("/echo/"):
        parsed_headers["Accept-Encoding"] = parsed_headers["Accept-Encoding"].split(", ")
        response = encoded_response(parsed_headers["Accept-Encoding"], path[6:])
        connection.sendall(response)
        return
    elif method == "GET" and path.startswith("/echo/"):
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(path[6:])}\r\n\r\n{path[6:]}"
    elif method == "GET" and path == "/user-agent":
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(parsed_headers["User-Agent"])}\r\n\r\n{parsed_headers["User-Agent"]}"        
    elif path.startswith("/files/") and get_file_contents(path[7:]) != False:
        content = get_file_contents(path[7:])
        response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(content)}\r\n\r\n{content}"
    elif method == "POST" and path.startswith("/files/"): 
        create_file(path[7:], body)
        response = "HTTP/1.1 201 Created\r\n\r\n"
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"

    # Send response to the client
    connection.sendall(response.encode())


if __name__ == "__main__":
    main()
