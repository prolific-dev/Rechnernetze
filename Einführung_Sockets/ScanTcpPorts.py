import socket
import threading

# SERVER_IP = '127.0.0.1'
SERVER_IP = '141.37.168.26'  # with vpn
PORTS = [*range(1, 51)]
OPEN_PORTS_DICT = {}
MESSAGE = 'Hello, World!'


def start_client(*args):
    port = args[0]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)

    try:
        print(f"Connecting to TCP server with IP {SERVER_IP} on Port {port}")
        sock.connect((SERVER_IP, port))
        print(f"Sending message {MESSAGE}")
        sock.send(MESSAGE.encode('utf-8'))
        msg = sock.recv(1024).decode('utf-8')
        OPEN_PORTS_DICT[port] = f"Message received; {msg}"
    except Exception as e:
        OPEN_PORTS_DICT[port] = e

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
