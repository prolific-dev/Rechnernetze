import socket
import time
import base64

def do_connect(sock: socket.socket, mail_server: tuple):

    print(f"Connecting to mail server {mail_server[0]} on Port {mail_server[1]}")
    sock.connect(mail_server)

    recv = sock.recv(1024)
    recv = recv.decode()
    print(f"Response: {recv}")

    if recv[:3] != '220':
        print("Connect not successful")
        quit()

def do_send(sock: socket.socket, msg: str, rsp_exc="0", wait_rsp=True):
    
    print(f"Sending {msg}")
    sock.send(msg)

    if wait_rsp:
        recv = sock.recv(1024)
        recv = recv.decode()
        print(f"Response: {recv}")

        if rsp_exc != "0" and recv[:3] != rsp_exc:
            print("Exception caught. Exiting program...")
            quit()


if __name__ == "__main__":
    MESSAGE     = "\r\n Meooooow!".encode()
    END_MESSAGE = "\r\n.\r\n".encode()
    MAIL_SERVER = ("asmtp.htwg-konstanz.de", 587)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    do_connect(sock, MAIL_SERVER)

    helo_command = "EHLO htwg-konstanz.de\r\n".encode()
    do_send(sock, helo_command, "250")

    username   = "rnetin"
    password   = "Ueben8fuer8RN"
    base64_str = (f"\x00{username}\x00{password}".encode())
    base64_str = base64.b64encode(base64_str)
    auth_msg   = "AUTH PLAIN ".encode() + base64_str + "\r\n".encode()
    do_send(sock, auth_msg)

    mail_from = "MAIL FROM: rntest@htwg-konstanz.de\r\n".encode()
    do_send(sock, mail_from)

    # Change rcpt address as you wish
    rcpt_to = "RCPT TO: example@htwg-konstanz.de\r\n".encode()
    do_send(sock, rcpt_to)

    data = "DATA\r\n".encode()
    do_send(sock, data)

    subject = "Subject: Testing my client\r\n\r\n".encode()
    do_send(sock, subject, wait_rsp=False)

    date = time.strftime("%a, %d %b %Y %H: %M: %S +0000", time.gmtime())
    date = (date + "\r\n\r\n").encode()
    do_send(sock, date, wait_rsp=False)
    do_send(sock, MESSAGE, wait_rsp=False)
    do_send(sock, END_MESSAGE)

    quit = "QUIT\r\n".encode()
    do_send(sock, quit)

    print("Closing socket")
    sock.close()



