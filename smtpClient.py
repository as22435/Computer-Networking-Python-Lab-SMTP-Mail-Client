from socket import socket, AF_INET, SOCK_STREAM

# Simple SMTP client for local testing / Gradescope
# Server must be local SMTP server at 127.0.0.1:1025

mailserver = '127.0.0.1'
port = 1025

sender = 'sender@example.com'
recipient = 'recipient@example.com'

subject = 'Test Email'
body = 'This is a test email from my SMTP client.'

# SMTP DATA section. It must end with \r\n.\r\n
msg = (
    'From: ' + sender + '\r\n' +
    'To: ' + recipient + '\r\n' +
    'Subject: ' + subject + '\r\n' +
    '\r\n' +
    body + '\r\n'
)
endmsg = '\r\n.\r\n'


def recv_reply(sock):
    """Receive server reply as a decoded string."""
    return sock.recv(1024).decode()


def send_command(sock, command):
    """Send one SMTP command and return the server reply."""
    sock.send(command.encode())
    return recv_reply(sock)


clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, port))

# Server greeting should usually be 220
recv = recv_reply(clientSocket)

# Say hello to the SMTP server
heloCommand = 'HELO localhost\r\n'
recv = send_command(clientSocket, heloCommand)

# Tell server who email is from
mailFromCommand = 'MAIL FROM:<' + sender + '>\r\n'
recv = send_command(clientSocket, mailFromCommand)

# Tell server who email is going to
rcptToCommand = 'RCPT TO:<' + recipient + '>\r\n'
recv = send_command(clientSocket, rcptToCommand)

# Start sending message data
# After DATA, server should reply once, then we send msg + endmsg.
dataCommand = 'DATA\r\n'
recv = send_command(clientSocket, dataCommand)

# Send the email headers/body and end with period line.
# Do not call recv before sending endmsg, or the program may hang.
clientSocket.send((msg + endmsg).encode())
recv = recv_reply(clientSocket)

# Quit cleanly
quitCommand = 'QUIT\r\n'
recv = send_command(clientSocket, quitCommand)

clientSocket.close()
