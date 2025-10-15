from socket import *
import ssl
import certifi


# Message to send
msg = "\r\n I love computer networks!"
endMsg = "\r\n.\r\n"

# Choose a mail server (e.g. mail.cse.lehigh.edu) and call it mailServer
mailServer = 'mail.cse.lehigh.edu'

# Create socket called clientSocket and establish a TCP connection with the mail server
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailServer, 25)) # port 25
recv = clientSocket.recv(1024).decode()
print('Connect: ', recv)
if recv[:3] != '220':
  print('220 reply not received from server.')
else:
    actualServerName = recv.split()[1] # get server name from response 

# Encrypting connectionw ith TLS
clientSocket.send('STARTTLS\r\n'.encode())
recv_starttls = clientSocket.recv(1024).decode()
print('STARTTLS response: ', recv_starttls)
if recv_starttls[:3] != '220':
    print('220 reply not received from server.')
else:
    context = ssl.create_default_context(cafile=certifi.where())
    secure_socket = context.wrap_socket(clientSocket, server_hostname=actualServerName)


# Send HELO command and print serverresponse.
heloCommand = 'HELO Piers\r\n'
secure_socket.send(heloCommand.encode())
recv1 = secure_socket.recv(1024).decode()
print('HELO response: ', recv1)
if recv1[:3] != '250':
   print('250 reply not received from server.')
 
# Send MAIL FROM command and print server response.
# Fill in start
mailFrom = 'MAIL FROM:<email@lehigh.edu>\r\n' # replace with your email
secure_socket.send(mailFrom.encode())
recv2 = secure_socket.recv(1024).decode()
print('MAIL FROM response: ', recv2)
if recv2[:3] != '250':
   print('250 reply not received from server.')
# Fill in end

# Send RCPT TO command and print server response.
# Fill in start
rcptTo = 'RCPT TO:<email@example.com>\r\n' # replace with recipient email
secure_socket.send(rcptTo.encode())
recv3 = secure_socket.recv(1024).decode()
print('RCPT TO response: ', recv3)
if recv3[:3] != '250':
   print('250 reply not received from server.')
# Fill in end

# Send DATA command and print server response.
# Fill in start
dataTo = 'DATA\r\n'
secure_socket.send(dataTo.encode())
recv4 = secure_socket.recv(1024).decode()
print('DATA response: ', recv4)
if recv4[:3] != '354': # expecting 354 for start mail input
    print('354 reply not received from server.')
# Fill in end

# Send message data.
# Fill in start
secure_socket.send(msg.encode())
# Fill in end

# Message ends with a single period.
# Fill in start
secure_socket.send(endMsg.encode())
recv5 = secure_socket.recv(1024).decode()
print('Message response: ', recv5)
if recv5[:3] != '250':
    print('250 reply not received from server.')
    secure_socket.close()
# Fill in end

# Send QUIT command and get server response.
# Fill in start
quitCommand = 'QUIT\r\n'
secure_socket.send(quitCommand.encode())
recv7 = secure_socket.recv(1024).decode()
print('QUIT response: ', recv7)
if recv7[:3] != '221': # 221 closing connection
    print('221 reply not received from server.')
secure_socket.close()
# Fill in end
