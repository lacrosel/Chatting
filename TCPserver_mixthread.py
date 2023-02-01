import socketserver
import json
import threading
import time
import random

import pygame

lock = threading.Lock()  # lock 선언


class UserManager:  # 유저 컨트롤용 클래스
    def __init__(self):
        self.users = {}  # 유저 데이터 수집용

    def addUser(self, username, cl_sock, addr):
        if username in self.users:
            # 받은 유저네임이 이미 존재하면
            # 현재 접속자에게 문자열 송신
            cl_sock.send('X!*!:!*!X'.encode())
            return None
        cl_sock.send('X!*!:!*!O'.encode())
        time.sleep(0.01)
        # 새로운 사용자를 등록함
        lock.acquire()  # Lock (사용자 등록 과정에서 다른 스레드랑 겹치지 않도록 lock
        self.users[username] = (cl_sock, addr)  # 유저네임을 키값 소켓정보와 아이피는 밸류값
        # client_socket, IP tuple로 저장(접속데이터니까 혹시 수정안되게)
        lock.release()  # Unlock

        # 모든 사용자에게 메시지 전송
        self.sendMessageToAll('C!*!:!*! [%s]님이 입장했습니다.' % username)
        time.sleep(0.01)
        print('▷ 대화 참여자 수 [%d]' % len(self.users))
        userList = []  # 참여인원 누구인지
        for name in self.users.keys():  # 키값이 username으로 채팅방에서 참여인원 출력용
            userList.append(name)
        print(userList)
        ulist = 'L!*!:!*!' + json.dumps(userList)  # json.dump메서드를 이용해서 리스트 바이너리화
        self.sendMessageToAll(ulist)
        '''
        참여인원 누구인지 확인용 아직 ui로 안해서 json으로 키값 자체 전송해도 ui에서 표현가능
        지금은 그냥 콘솔창에서 출력하도록 했기 때문에 보기 좋게 하려고 반복문으로 print함'''
        return username

    def removeUser(self, username):
        # 삭제하려는 ID가 없으면 아무일도 안함.
        if username not in self.users:
            return

        lock.acquire()  # Lock
        del self.users[username]  # Dictionary에서 아이디에 해당하는 항목 삭제
        lock.release()  # Unlock

        self.sendMessageToAll('C!*!:!*! [ %s ]님이 퇴장했습니다.' % username)
        time.sleep(0.001)
        print('▷ 대화 참여자 수 [%d]' % len(self.users))
        userList = []  # 참여인원 누구인지
        for name in self.users.keys():  # 키값이 username으로 채팅방에서 참여인원 출력용
            userList.append(name)
        print(userList)
        ulist = 'L!*!:!*!' + json.dumps(userList)  # json.dump메서드를 이용해서 리스트 바이너리화
        self.sendMessageToAll(ulist)

    def gamesignal(self, to, msg):
        sock = self.users[to][0]
        sock.send(msg)

    def messageHandler(self, username, msg):
        if msg[1].strip() == 'E!X@I#T%':  # 클라가 특정 문자(신호) 보내면 disconnect으로 인식해서
            self.removeUser(username)  # 클라리스트에서 삭제
            return -1  # server 클래스에서 접속해제 확인용 신호 전달

        self.sendMessageToAll(f'{msg[0]}!*!:!*![%s] %s' % (username, msg[1]))  # send메서드 호출

    def sendMessageToAll(self, msg):  # 접속한 모두에게 메시지 보내는 메서드
        # Dictionary 값 2개 추출: client_sock, IP로 구성된 tuple 값 위에서 설명함.
        for cl_sock, addr in self.users.values():
            cl_sock.send(msg.encode())  # 각각의 사용자에게 메시지 전송

    def dongGameset(self, msg):
        Cmsg = msg.decode().split('!*!:!*!')
        sendlist = []
        for i in range(5):
            a = random.randint(50, int(Cmsg[2]) - 50)
            b = random.randint(3, 9)
            sendlist.append([a, b])
        print('qhsosek', sendlist)
        slist = 'Gc!*!:!*!dongset!*!:!*!' + json.dumps(sendlist)
        self.users['qwe'][0].send(slist.encode())
        self.users['asd'][0].send(slist.encode())
        return slist

    def dongre(self):
        a = random.randint(50, 600 - 50)
        b = random.randint(3, 9)
        sendlist = [a, b]
        slist = 'Gc!*!:!*!dongset!*!:!*!' + json.dumps(sendlist)
        self.users['qwe'][0].send(slist.encode())
        self.users['asd'][0].send(slist.encode())


class gameserver:
    def __init__(self):
        self.gameroom = {}


    def entranceRoom(self, user, roomname):
        try:
            self.gameroom[roomname].append(user)
            print(self.gameroom)
        except KeyError:
            self.gameroom[roomname] = []
            self.gameroom[roomname].append(user)
            print(self.gameroom)

    def exitRoom(self, user, roomname):
        print('1', self.gameroom[roomname])
        self.gameroom[roomname].remove(user)
        print('2', self.gameroom[roomname])
        if len(self.gameroom[roomname]) == 0:
            del self.gameroom[roomname]
        print(self.gameroom)
    def RoomUserlist(self, roomname, userlist):
        aa = self.gameroom[roomname]
        senddata = json.dumps(aa)
        for i in aa:
            userlist[i][0].send(f'Gr!*!:!*!{senddata}*'.encode())
        print('게임방 유저 보낸다~')
        print(self.gameroom)
class TCPhandler(socketserver.BaseRequestHandler):
    userManager = UserManager()  # 유저 클래스 선언
    gameServer = gameserver()

    def setup(self):
        self.username = self.registerUsername()  # 사용자 id 처리

    def handle(self):  # 클라에서 신호 보낼시 자동으로 동작
        try:
            msg = self.request.recv(1024)  # 접속된 사용자로부터 입력대기
            while msg:
                # print(msg.decode())  # 서버 화면에 출력
                Cmsg = msg.decode().split('!*!:!*!')
                print('Cmsg', Cmsg)
                if Cmsg[0] == 'C':
                    if self.userManager.messageHandler(self.username, Cmsg) == -1:
                        self.request.close()  # disConnection
                        break  # recv 종료
                elif Cmsg[0] == 'G':
                    self.userManager.gamesignal(Cmsg[2], msg)
                elif Cmsg[0] == 'Gc':
                    if Cmsg[1] == 'dongset' and Cmsg[3] == '1':
                        slist = self.userManager.dongGameset(msg)
                        # self.request.send(slist.encode())
                    elif Cmsg[1] == 'redong' and Cmsg[2][1] == '1':
                        self.userManager.dongre()
                elif Cmsg[0] == 'Gr':
                    if Cmsg[2][-1:] == '@':
                        self.gameServer.entranceRoom(Cmsg[1], Cmsg[2][:-1])
                        self.gameServer.RoomUserlist(Cmsg[2][:-1], self.userManager.users)
                    elif Cmsg[2][-1:] == '#':
                        print('s나감')
                        self.gameServer.exitRoom(Cmsg[1], Cmsg[2][:-1])
                        self.gameServer.RoomUserlist(Cmsg[2][:-1], self.userManager.users)
                msg = self.request.recv(1024)  # 메시지 수신 대기

        except Exception as e:  # 어떤 에러 일지 모르니까 표시만 하고 서버 멈추지는 않도록 처리.
            print(e)

        print('▷ [%s] disConnection' % self.client_address[0])
        self.userManager.removeUser(self.username)  # 클라 삭제처리

    def registerUsername(self):  # 접속자의 이름 받기
        while True:
            # self.request.send('로그인ID: '.encode())  # 신규 현재 접속자에게 전송
            username = self.request.recv(1024)  # 수신 대기
            username = username.decode().strip()  # strip(): 공백 제거
            if self.userManager.addUser(username, self.request, self.client_address):
                # 네임, 소켓정보, 주소 파라미터로 클라 추가
                return username


# socketserver.ThreadingMixIn: 독립된 스레드로 처리하도록 접속시 마다 새로운 스레드 생성
# 직접적으로 스레드 동작하게 지정해주는거랑 같다. 대신 이미 누가 메서드로 만들어 놓은거 사용하는 것.
# ThreadingMixIn(소켓서버 스레드 동작), TCPServer class(스레드 동작시킬 위에서 정의한 TCPserver) 상속
class ChatingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass  # 이건 단순하게 스레드 동작 하게 한다는 거니까 특별히 뭘 적어줄 필요 x



if __name__ == "__main__":
    address = ("10.10.21.106", 9009)

    print('▷ 채팅 서버를 시작합니다.')
    print('▷ 채팅 서버를 끝내려면 Ctrl-C를 누르세요.')

    try:
        server = ChatingServer(address, TCPhandler)
        server.serve_forever()  # 무한 실행
    except KeyboardInterrupt:  # Ctrl + C 입력시 종료
        print('▷ 채팅 서버를 종료합니다.')
        server.shutdown()  # 서버 종료
        server.server_close()  # 메모리 해제
