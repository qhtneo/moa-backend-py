import socketserver

class MyHandler(socketserver.BaseRequestHandler):
    # 접속 유저 관리
    users = {}
    def sendToAll(self, msg):
        for sock, addr in self.users.values():
            sock.send(msg.encode())
            
    def addUser(self, nickname, c_sock, addr):
        # 이미 등록된 닉네임인 경우
        if nickname in self.users:
            c_sock.send("이미 등록된 닉네임 입니다.\n".encode())
            return False
        
        # 새로운 유저인 경우
        self.users[nickname] = (c_sock, addr)
        self.sendToAll(f"[{nickname}]님이 입장 했습니다.")
        print(f"현재 참여중 {len(self.users)}명")
        return True
    
    def handle(self):
        print(f"[{self.client_address[0]}] 접속 연결됨")
        
        while True:
            # send 함수는 바이트 형태로 인코딩 해야만 보내짐
            self.request.send("채팅 닉네임을 입력하세요: ".encode())
            # recv로 들어온 데이터는 바이트형태이기 때문에 디코딩 필요
            nickname = self.request.recv(1024).decode()
            if self.addUser(nickname, self.request, self.client_address):
                break
        try:
            while True:
                msg = self.request.recv(1024)
                print(msg)
                self.sendToAll(f"[{nickname}] {msg.decode()}")
        finally:
            print(f"[{nickname}] 연결이 끊어졌습니다.")
            del self.users[nickname]
            self.sendToAll(f"[{nickname}]님이 퇴장했습니다.")

class ChatServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

chat = ChatServer(("", 9700), MyHandler)
try:
    chat.serve_forever()
except KeyboardInterrupt:
    print("서버를 종료합니다.")
finally:
    chat.shutdown()
    chat.server_close()


# sock = socketserver.TCPServer(("", 9700), MyHandler)
# sock.serve_forever()
