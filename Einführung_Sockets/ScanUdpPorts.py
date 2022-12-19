import socket
import threading
import time

SERVER_IP = '127.0.0.1'
PORTS = [*range(1, 51)]
MESSAGE = 'Hello, World!'


def start_client(*args):
    port = args[0]
    print(f"Sending message {MESSAGE} to UDP server with IP {SERVER_IP} on Port {port}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3)

    try:
        sock.sendto(MESSAGE.encode('utf-8'), (SERVER_IP, port))

        try:
            data, addr = sock.recvfrom(1024)
            print(f"received message: {data.decode('utf-8')} from {addr}")
        except socket.timeout:
            print(f"Socket timed out at {time.asctime()}")

        sock.close()
    except:
        print(f'could not connect to port {port}')


def main():
    threads = []
    for port in PORTS:
        thread = threading.Thread(target=start_client, args=[port])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()
