import socket
from struct import *

SERVER_IP   = '127.0.0.1'
SERVER_PORT = 50000

def my_sum(values: tuple) -> int:
    sum = 0
    for x in values:
        sum += x
    return sum

def my_multiply(values: tuple) -> int:
    product = 1
    for x in values:
        product *= x
    return product

def my_min(values: tuple) -> int:
    min = values[0]
    for x in values:
        if x < min:
            min = x
    return min

def my_max(values: tuple) -> int:
    max = values[0]
    for x in values:
        if x > max:
            max = x
    return max

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    sock.settimeout(30)
    sock.listen(1)
    print(f"Server now listening on port {SERVER_PORT}")

    client_sock, client_addr = sock.accept()
    recv = client_sock.recv(1024)

    d_id   = unpack("!I", recv[0:4])[0]
    d_op   = unpack("!s", recv[4:5])[0].decode('utf-8')
    d_num  = unpack("!I", recv[5:9])[0]
    d_list = unpack("!{}i".format(d_num), recv[9:])

    result = 0

    if   d_op == 's':
        result = my_sum(d_list)
    elif d_op == 'm':
        result = my_multiply(d_list)
    elif d_op == 'i':
        result = my_min(d_list)
    elif d_op == 'a':
        result = my_max(d_list)
    else:
        print("No operation defined. Returning -1.")
    
    e_id     = pack("!I", d_id)
    e_result = pack("!i", result)
    encoded  = e_id + e_result 

    print("Sending echo data back to client.")
    client_sock.send(encoded)

    sock.close()
    

