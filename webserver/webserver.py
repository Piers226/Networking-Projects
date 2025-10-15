# Piers Rajguru 9/29/25 Programming 1
from socket import *


serv_sock = socket(
    AF_INET, 
    SOCK_STREAM,
    proto=0)

host_addr = '127.0.0.1' #using localhost
port = 8080
serv_sock.bind((host_addr, port))
serv_sock.listen(10) # server starts listening on port 8080
print(f"Server running on {host_addr} port {port}")
try:
    while True:
        connection_sock, addr = serv_sock.accept() # create a socket for client connections, start accepting responces
        try:
            request = connection_sock.recv(1024).decode()
            #print("Request:", request)
            #LOGGING
            # parse request, to log the request details
            request_line = request.splitlines()[0] if request else ""
            parts = request_line.split()
            if len(parts) >= 2:
                method = parts[0]
                url = parts[1]
            else:
                method = "UNKNOWN"
                url = ""
            print("\nRequest Method:", method)
            print(f"Requested URL: {host_addr}{url}")

            #Parse filename
            parts = request.split()
            if len(parts) > 1:
                filename = parts[1].lstrip("/")
            else: #by default, show index.html
                filename = "index.html"
            
            #print("file: ",filename)
            # Default to index.html if root or directory
            if filename == "" or filename.endswith("/"):
                filename += "index.html"

            # Always serve from static/ so append to filename
            filepath = "static/" + filename
            with open(filepath, "r") as f:
                body = f.read()
            
            header = "HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n"
            connection_sock.sendall(header.encode() + body.encode())
            print("Status Code: 200 OK") # unless there is an error, return 200
        except FileNotFoundError: # else return 404
            error_msg = "<h1>404 Not Found</h1>"
            connection_sock.sendall(b"HTTP/1.0 404 Not Found\r\nContent-Type: text/html\r\n\r\n")
            connection_sock.sendall(error_msg.encode())
            print("Status Code: 404 Not Found")
        finally:
            connection_sock.close()
except KeyboardInterrupt:
    print("Shutting down server...")
finally: # always close socket
    serv_sock.close()