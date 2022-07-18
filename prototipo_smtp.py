from socket import *
import base64

# Mail content
subject = "I love computer networks!"
contenttype = "text/plain"
msg = "I love computer networks!"
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver 
# If you don't know, just search the University / enterprise mailbox server directly, most of which are 25 port sending ports
mailserver = "mail.labredes.info"

# Sender and reciever
fromaddress = "cassia"
toaddress = "hector@labredes.info"

# Auth information (Encode with base64)
username = base64.b64encode(fromaddress.encode()).decode()
password = base64.b64encode("123456".encode()).decode()


# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM) 
clientSocket.connect((mailserver, 587))

recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')


# Auth must be authorized after hello
clientSocket.sendall('AUTH LOGIN\r\n'.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if (recv[:3] != '334'):
	print('334 reply not received from server')

clientSocket.sendall((username + '\r\n').encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if (recv[:3] != '334'):
	print('334 reply not received from server')

clientSocket.sendall((password + '\r\n').encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if (recv[:3] != '235'):
	print('235 reply not received from server')

# Send MAIL FROM command and print server response.
# Fill in start
#sendall will send all the data until the error or all the data are sent, and send will send less than the required number of bytes
clientSocket.sendall(('MAIL FROM: <'+fromaddress+'>\r\n').encode())
recv2 = clientSocket.recv(1024).decode()
print(recv2)
if (recv2[:3] != '250'):
    print('250 reply not received from server.')
# Fill in end

# Send RCPT TO command and print server response. 
# Fill in start the command here is wrong. It's not MAIL, it's RCPT
clientSocket.sendall(('RCPT TO: <'+toaddress+'>\r\n').encode())
recv3 = clientSocket.recv(1024).decode()
print(recv3)
if (recv3[:3] != '250'):
    print('250 reply not received from server.')

# Fill in end
# Send DATA command and print server response. 
# Fill in start
clientSocket.send(('DATA\r\n').encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if (recv[:3] != '354'):
    print('354 reply not received from server')
# Fill in end

# Send message data.
# Fill in start
message = 'from:' + fromaddress + '@labredes.info' + '\r\n'
message += 'to:' + toaddress + '\r\n'
message += 'subject:' + subject + '\r\n'
message += 'Content-Type:' + contenttype + '\r\n'
message += '\r\n' + msg
clientSocket.sendall(message.encode())

# Fill in end
# Message ends with a single period.
# Fill in start
clientSocket.sendall(endmsg.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if (recv[:3] != '250'):
	print('250 reply not received from server')
# Fill in end
# Send QUIT command and get server response.
# Fill in start
clientSocket.sendall('QUIT\r\n'.encode())
# Fill in end

clientSocket.close()