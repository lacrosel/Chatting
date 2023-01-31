import socket
import sys
import time
import threading
import pyautogui
from PyQt5 import uic
from PyQt5.QtWidgets import *
import pygame
import json
import random
import os

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

        address = ("10.10.21.106", 9009)
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
                if msg[0] == 'X':
                    if msg[1] == 'X':
                        QMessageBox.information(self, "알림", "이미 존재하는 닉네임입니다.")
                        self.running = False
                        break
                    elif msg[1] == 'O':
                        self.CHAT_STACK.setCurrentIndex(1)
                if msg[0] == 'C':
                    self.listWidget.addItem(msg[1])
                    self.scollcheck()
                if msg[0] == 'G':
                    print(msg)
                    if (msg[1] == 'right'):
                        self.p2_dx = 10
                    elif (msg[1] == 'left'):
                        self.p2_dx = -10
                    elif (msg[1] == 'zero'):
                        self.p2_dx = 0
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

        size = [600, 800]
        screen = pygame.display.set_mode(size)

        done = False
        clock = pygame.time.Clock()

        self.runGame(size, screen, done, clock)
        pygame.quit()

    def runGame(self, size, screen, done, clock):
        dung_image = pygame.image.load('../ddong.png')
        dung_image = pygame.transform.scale(dung_image, (50, 50))
        dungs = []

        for i in range(5):
            rect = pygame.Rect(dung_image.get_rect())
            rect.left = random.randint(0, size[0])
            rect.top = -100
            dy = random.randint(3, 9)
            dungs.append({'rect': rect, 'dy': dy})

        character1_image = pygame.image.load('../character1.png')
        character1_image = pygame.transform.scale(character1_image, (70, 70))
        character = pygame.Rect(character1_image.get_rect())
        character.left = size[0] // 2 - character.width // 2
        character.top = size[1] - character.height
        character_dx = 0

        character2_image = pygame.image.load('../character2.png')
        character2_image = pygame.transform.scale(character2_image, (70, 70))
        character2 = pygame.Rect(character2_image.get_rect())
        character2.left = size[0] // 2 - character2.width // 2
        character2.top = size[1] - character2.height
        self.p2_dx = 0


        while not done:
            clock.tick(40)
            screen.fill((0, 0, 0))

            if self.start_sginal:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                        break
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            character_dx = -10
                            msg = 'G' + '!*!:!*!' + "left" + '!*!:!*!' + 'asd'
                            self.sock.sendall(msg.encode())  # 클라이언트에게 내가내린명령전송
                        elif event.key == pygame.K_RIGHT:
                            character_dx = 10
                            msg = 'G' + '!*!:!*!' + "right" + '!*!:!*!' + 'asd'
                            self.sock.sendall(msg.encode())  # 클라이언트에게 내가내린명령전송
                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT:
                            character_dx = 0
                            msg = 'G' + '!*!:!*!' + "zero" + '!*!:!*!' + 'asd'
                            self.sock.sendall(msg.encode())  # 클라이언트에게 내가내린명령전송
                        elif event.key == pygame.K_RIGHT:
                            character_dx = 0
                            msg = 'G' + '!*!:!*!' + "zero" + '!*!:!*!' + 'asd'
                            self.sock.sendall(msg.encode())  # 클라이언트에게 내가내린명령전송

                for dung in dungs:
                    dung['rect'].top += dung['dy']
                    if dung['rect'].top > size[1]:
                        dungs.remove(dung)
                        rect = pygame.Rect(dung_image.get_rect())
                        rect.left = random.randint(0, size[0])
                        rect.top = -100
                        dy = random.randint(3, 9)
                        dungs.append({'rect': rect, 'dy': dy})

                character.left = character.left + character_dx
                character2.left = character2.left + self.p2_dx
                if character.left < 0:
                    character.left = 0
                elif character.left > size[0] - character.width:
                    character.left = size[0] - character.width

                screen.blit(character1_image, character)
                screen.blit(character2_image, character2)
                for dung in dungs:
                    if dung['rect'].colliderect(character):
                        done = False
                    screen.blit(dung_image, dung['rect'])
            else:
                pass
            pygame.display.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Cclient()
    sys.exit(app.exec_())
