import socket
import sys
import time
from _thread import *
from threading import Thread
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import json

testui = uic.loadUiType("ui/chat.ui")[0]


class Cclient(QWidget, testui):
    def __init__(self):
        super().__init__()
        # self.HOST = input("접속할 서버 IP    ")
        self.name = ''
        self.setupUi(self)
        self.show()
        self.CHAT_STACK.setCurrentIndex(3)
        self.running = False
        # 연결 서버 정보
        # self.signal = {'c':}
        self.connection.clicked.connect(self.admission)
        self.CHAT_BT_tsend.clicked.connect(self.sendMsg)
        self.CHAT_LE_tsend.returnPressed.connect(self.sendMsg)
        self.CHAT_timeExit.clicked.connect(self.CHAT_exit)

    def admission(self):
        self.running = True
        self.name = self.nameedit.text()
        self.nameedit.clear()
        self.CHAT_STACK.setCurrentIndex(1)
        HOST = '10.10.21.106'
        PORT = 9009
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))
        th = Thread(target=self.recvMsg, args=(self.sock,))
        th.daemon = True
        th.start()
        # self.sock.send('1'.encode())
        self.sock.send(self.name.encode())

    # def runChat(host, port):
    #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    #         '''
    #         따로 소켓 close 안하도록 with 사용
    #         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         sock.close()
    #         합쳐 놓은 거랑 같다.
    #         '''
    #         sock.connect((host, port))  # 소켓 연결
    #         # rcvMsg 함수를 연속 실행하는 스레드 생성,
    #         # sock 소켓 객체를 tuple 형식으로 전달
    #         t_msg = Thread(target=recvMsg, args=(sock,))  # 파라미터 1개인데 왜 , 찍는지는 튜플 기본 형태 확인
    #         t_msg.daemon = True  # 스레드를 생성한 메인 스레드가 종료되면 자동으로 종료됨.
    #         t_msg.start()  # 스레드 시작
    #
    #         while True:
    #             msg = input()  # 키보드 입력
    #             if msg == '!e!x!i!t!':  # 종료
    #                 sock.send(msg.encode())
    #                 break
    #                 # while 종료 - with로 소켓을 열었기 때문에 runChat 메서드가 끝나면서 자동으로 소켓 close됨.
    #
    #             sock.send(msg.encode())  # 입력 메시지 전송

    def userList_set(self, ulist):
        self.CHAT_userlist.clearContents()
        self.CHAT_userlist.setRowCount(len(ulist))
        self.CHAT_userlist.setColumnCount(1)

        for row in range(len(ulist)):
            self.CHAT_userlist.setItem(row, 0, QTableWidgetItem(ulist[row]))

    def sendMsg(self):
        message = 'C' + '!*!:!*!' + self.CHAT_LE_tsend.text()
        if self.CHAT_LE_tsend.text() == "" or self.CHAT_LE_tsend.text() is None:
            return
        self.sock.send(message.encode())
        self.CHAT_LE_tsend.clear()

    def recvMsg(self, sock):  # 원
        while True:  # 연속성 스레드
            try:
                data = sock.recv(1024)  # 서버로부터 문자열 수신
                if not data:  # 문자열 없으면 종료
                    break
                print(data.decode())
                msg = data.decode().split('!*!:!*!')
                print(msg)
                if msg[0] == 'C':
                    self.listWidget.addItem(msg[1])
                    self.scollcheck()
                if msg[0] == 'G':
                    pass
                if msg[0] == 'L':
                    print('제이슨!')
                    ulist = json.loads(msg[1])  # bytes형으로 수신된 데이터를 문자열로 변환 출력 json.loads
                    self.userList_set(ulist)
            except:
                pass  # 예외 원인 무시
            if not self.running:
                break
        self.sock.close()
        print("중지")

    def scollcheck(self):
        time.sleep(0.005)
        self.listWidget.scrollToBottom()

    def CHAT_exit(self):
        self.running = False
        message = 'C' + '!*!:!*!' + 'E!X@I#T%'
        print("asd")
        self.sock.send(message.encode())
        time.sleep(1)
        self.listWidget.clear()
        self.CHAT_STACK.setCurrentIndex(3)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Cclient()
    sys.exit(app.exec_())
