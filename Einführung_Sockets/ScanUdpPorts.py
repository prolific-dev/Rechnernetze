import socket
import threading
import time

#SERVER_IP = '127.0.0.1'
SERVER_IP = '141.37.168.26' # with vpn
PORTS = [*range(1, 51)]
OPEN_PORTS_DICT = {}
MESSAGE = 'Hello, World!'


def start_client(*args):
    port = args[0]
    print(f"Sending message {MESSAGE} to UDP server with IP {SERVER_IP} on Port {port}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3)

    try:
        sock.sendto(MESSAGE.encode('utf-8'), (SERVER_IP, port))
        data, addr = sock.recvfrom(1024)
        print(f"received message: {data.decode('utf-8')} from {addr}")
    except Exception as e:
        OPEN_PORTS_DICT[port] = e
        return

    OPEN_PORTS_DICT[port] = 'Open'
    sock.close()


def main():
    threads = []
    for port in PORTS:
        thread = threading.Thread(target=start_client, args=[port])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print('result:')
    for port, status in sorted(OPEN_PORTS_DICT.items()):
        print(f'Port {port}: {status}')


if __name__ == '__main__':
    main()
