import socket
import sys
import time
import threading
import pyautogui
from PyQt5 import uic
from PyQt5.QtWidgets import *
import pygame
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
        self.CHAT_game.clicked.connect(self.test)

    def admission(self):
        self.running = True
        self.name = self.nameedit.text()
        self.nameedit.clear()
        self.CHAT_STACK.setCurrentIndex(1)
        address = ("192.168.0.4", 9009)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((address))
        th = threading.Thread(target=self.recvMsg, args=(self.sock,))
        th.daemon = True
        th.start()
        self.sock.send(self.name.encode())

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
                    print(msg)
                    if (msg[1] == 'up'):  # 소켓으로부터받은데이터가 up일경우 적y좌표조정
                        self.p2_y -= 3
                    elif (msg[1] == 'down'):  # 소켓으로부터받은데이터가 down일경우 적y좌표조정
                        self.p2_y += 3
                    elif (msg[1] == 'right'):  # 소켓으로부터받은데이터가 right일경우 적x좌표조정
                        self.p2_x += 3
                    elif (msg[1] == 'left'):  # 소켓으로부터받은데이터가 left일경우 적x좌표조정
                        self.p2_x -= 3
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

    def test(self):
        self.pygaming_test()

    def pygaming_test(self):
        pygame.init()  # 2. pygame 초기화

        # 3. pygame에 사용되는 전역변수 선언
        WHITE = (255, 255, 255)
        size = [400, 500]
        screen = pygame.display.set_mode(size)

        done1 = False
        done2 = False
        clock = pygame.time.Clock()

        # pygame에 사용하도록 비행기 이미지를 호출
        airplane1 = pygame.image.load('test.png')
        airplane1 = pygame.transform.scale(airplane1, (60, 45))
        airplane2 = pygame.image.load('test.png')
        airplane2 = pygame.transform.scale(airplane2, (60, 45))

        th_game1 = threading.Thread(target=self.runGame2, args=(clock, screen, WHITE, done2, airplane2))
        th_game1.daemon = True
        th_game1.start()

        self.runGame(clock, screen, WHITE, done1, airplane1)

        pygame.quit()

        # 4. pygame 무한루프

    def runGame(self, clock, screen, WHITE, done, airplane):
        x = 20
        y = 24
        while not done:
            clock.tick(20)
            screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                # 방향키 입력에 대한 이벤트 처리
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        pyautogui.keyUp('up')
                        y -= 3
                        msg = 'G' + '!*!:!*!' + "up" + '!*!:!*!' + 'asd'
                        self.sock.sendall(msg.encode())  # 클라이언트에게 내가내린명령전송
                    elif event.key == pygame.K_DOWN:
                        pyautogui.keyUp('down')
                        y += 3
                        msg = 'G' + '!*!:!*!' + "down" + '!*!:!*!' + 'asd'
                        self.sock.sendall(msg.encode())
                    elif event.key == pygame.K_RIGHT:
                        pyautogui.keyUp('right')
                        x += 3
                        msg = 'G' + '!*!:!*!' + "right" + '!*!:!*!' + 'asd'
                        self.sock.sendall(msg.encode())
                    elif event.key == pygame.K_LEFT:
                        pyautogui.keyUp('left')
                        x -= 3
                        msg = 'G' + '!*!:!*!' + "left" + '!*!:!*!' + 'asd'
                        self.sock.sendall(msg.encode())

            screen.blit(airplane, (x, y))
            pygame.display.update()

    def runGame2(self, clock, screen, WHITE, done, airplane):
        self.p2_x = 20
        self.p2_y = 24

        while not done:
            clock.tick(20)
            screen.fill(WHITE)

            if done:
                break
            screen.blit(airplane, (self.p2_x, self.p2_y))
            pygame.display.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Cclient()
    sys.exit(app.exec_())
