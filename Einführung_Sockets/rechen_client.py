import socket
from struct import *
from typing import List

SERVER_IP   = '127.0.0.1'
SERVER_PORT = 50000

if __name__ == "__main__":

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))
    
    s_list = [1, 2, 3, 4]
    s_id   = 14
    s_op   = 's'.encode('utf-8') # s = summe, m = multiplikation, i = min, a = max
    s_num  = len(s_list)

    e_id   = pack("!I", s_id)
    e_op   = pack("!s", s_op)
    e_num  = pack("!I", len(s_list))
    e_list = pack("!{}i".format(len(s_list)), *s_list)
    encoded = e_id + e_op + e_num + e_list

    print("Sending data to server.")
    sock.send(encoded)

    recv = sock.recv(1024)
    d_id = unpack("!I", recv[0:4])[0]
    d_result = unpack("!i", recv[4:])[0]
    print(f"Result ({d_id}) = {d_result}")

    sock.close()

    

