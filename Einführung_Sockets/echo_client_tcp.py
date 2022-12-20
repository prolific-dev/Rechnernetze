import socket
import time

# Server_IP   = '127.0.0.1'
# Server_PORT = 50000
Server_IP = '141.37.168.26'
Server_PORT = 7
MESSAGE = 'Hello, World!'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(10)

print(f"Connecting to TCP server with IP {Server_IP} on Port {Server_PORT}")
sock.connect((Server_IP, Server_PORT))

print(f"Sending message {MESSAGE}")
sock.send(MESSAGE.encode('utf-8'))

try:
    msg = sock.recv(1024).decode('utf-8')
    print(f"Message received; {msg}")
except socket.timeout:
    print(f"Socket timed out at {time.asctime()}")

sock.close()
