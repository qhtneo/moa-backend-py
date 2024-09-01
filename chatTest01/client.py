import socket
from threading import Thread

def recvMessage(sock):
    while True:
        msg = sock.recv(1024)
        print(msg.decode())

print("1. 소켓생성")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("3. 접속시도")
sock.connect(("127.0.0.1", 9700))

th = Thread(target=recvMessage, args = (sock, ))
th.daemon=True
th.start()

while True:
    msg = input("입력 (종료하려면 'quit' 입력): ")
    if msg.lower() == "quit":
        print("연결을 종료합니다.")
        sock.close()
        break
    sock.send(msg.encode())

print("5. 데이터 송신")
sock.sendall(bytes("Hello socket", "utf-8"))

print("6. 접속 종료")
sock.close()
