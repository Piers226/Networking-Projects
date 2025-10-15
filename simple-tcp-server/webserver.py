import socket



serv_sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
    proto = 0
)

#print(type(serv_sock))
serv_sock.bind(('127.0.0.1', 6543))

backlog = 10 # setting max number of queued connections
serv_sock.listen(backlog) # Put the server socket in listening state

while True:
# obtain established connection from backlog queue
    client_sock, client_addr = serv_sock.accept()
    print('New Connection from', client_addr)
    chunks=[]
    while True:
        data = client_sock.recv(2048)
        if not data:
            break
        
        chunks.append(data)

    client_sock.sendall(b''.join(chunks))
    client_sock.close()



# data = client_sock.recv(2048)
# client_sock.send(data)

# serv_sock.close()
# client_sock.close()
# client_addr.close()