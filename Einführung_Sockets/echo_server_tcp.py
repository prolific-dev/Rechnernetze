import socket
import time

My_IP                  = '127.0.0.1' # Lokale IP
My_PORT                = 50000       # Lokaler Port
server_activity_period = 30          # Zeit, wie lange der Server aktiv sein soll

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((My_IP, My_PORT))
print(f"Listening on Port {My_PORT} for incoming TCP connections");

# Ende der Aktivitätsperiode
t_end = time.time() + server_activity_period

sock.listen(1)
print('Listening ...')

while time.time() < t_end:
    try:
        conn, addr = sock.accept()
        print(f"Incoming connection accepted: {addr}")
        break
    except socket.timeout:
        print(f"Socket timed out listening {time.asctime()}")

while time.time() < t_end:
    try:
        data = conn.recv(1024)
        # receiving empty messages means that the socket other side closed the socket
        if not data: 
            print('Connection closed from other side')
            print('Closing ...')
            conn.close()
            break
        print(f"received message: {data.decode('utf-8')} from {addr}")
        conn.send(data[::-1])
    except socket.timeout:
        print(f"Socket timed out at {time.asctime()}")

sock.close()

if conn:
    conn.close()
