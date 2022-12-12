import socket
import time

My_IP                  = "127.0.0.1" # Lokale IP
My_PORT                = 50000       # Lokaler Port
server_activity_period = 30          # Zeit, wie lange der Server aktiv sein soll

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((My_IP, My_PORT))
sock.settimeout(10)

# Ende der Aktivitätsperiode
t_end=time.time() + server_activity_period

while time.time()<t_end:
    try:
        data, addr = sock.recvfrom(1024) 
        print(f"received message: {data.decode('utf-8')} from {addr}")
        sock.sendto(data[::-1],addr)
    except socket.timeout:
        print(f"Socket timed out at {time.asctime()}")

sock.close()
