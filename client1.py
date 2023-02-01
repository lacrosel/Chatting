import socket
import sys
import time
import threading
import pyautogui
from PyQt5 import uic
from PyQt5.QtCore import QThread
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
        self.F_gamecreate.hide()

        self.CHAT_BT_close2.clicked.connect(lambda: self.pageReset(1))
        self.create_cancel.clicked.connect(lambda: self.pageReset(2))
        self.create_agree.clicked.connect(self.test)
        self.CHAT_gamecreate.clicked.connect(self.gameCreate_check)

        self.connection.clicked.connect(self.admission)
        self.CHAT_BT_tsend.clicked.connect(self.sendMsg)
        self.CHAT_LE_tsend.returnPressed.connect(self.sendMsg)
        self.CHAT_timeExit.clicked.connect(self.CHAT_exit)

        # self.CHAT_game.clicked.connect(self.test)

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
                    if msg[1] == 'right':
                        self.p2_dx = 10
                    elif msg[1] == 'left':
                        self.p2_dx = -10
                    elif msg[1] == 'zero':
                        self.p2_dx = 0
                # if msg[0] == 'Gc':
                #     print("동데이터!")
                #     if msg[1] == 'dongset':
                #         self.poss = json.loads(msg[2])
                #         print(self.poss)
                #         self.pygaming_test()
                #     elif msg[1] == 'redong':
                #         print('동이다')
                #         self.rposs = json.loads(msg[2])
                if msg[0] == 'Gr':
                    if msg[1][-1] == '*':
                        print('rasrasrrrrrrrrr')
                        self.gru_list = json.loads(msg[1][:-1])
                        self.gameroomset(1)

                if msg[0] == 'L':
                    print('제이슨!')
                    ulist = json.loads(msg[1])  # bytes형으로 수신된 데이터를 문자열로 변환 출력 json.loads
                    self.userList_set(ulist)
            except Exception as e:  # 어떤 에러 일지 모르니까 표시만 하고 서버 멈추지는 않도록 처리.
                print(e)
            if not self.running:
                break
        self.sock.close()
        print("중지")

    def gameCreate_check(self):
        self.F_gamecreate.show()
    def gameroomset(self, signal):
        if signal == 1:
            self.CHAT_STACK.setCurrentIndex(2)

            print(len(self.gru_list))
            # self.Game_userlist
            self.Game_userlist.clearContents()
            self.Game_userlist.setRowCount(len(self.gru_list))
            self.Game_userlist.setColumnCount(1)

            for i in range(len(self.gru_list)):
                self.Game_userlist.setItem(i, 0, QTableWidgetItem(self.gru_list[i]))

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
        if self.game_name.text() is None or self.game_ppcb.currentIndex() == 0 or self.game_gamecb.currentIndex() == 0:
            a = QMessageBox.information(self, "알림", "정보를 확인 해주세요.")
            return
        self.roomname = self.game_name.text()
        self.sock.send(f'Gr!*!:!*!{self.name}!*!:!*!{self.roomname}@'.encode())

    def pageReset(self, signal):
        if signal == 1:
            self.Game_userlist2.clear()
            self.Game_userlist.clear()
            self.gr_chat.clear()
            self.gr_sendtext.clear()
            self.CHAT_STACK.setCurrentIndex(1)
            self.sock.send(f'Gr!*!:!*!{self.name}!*!:!*!{self.roomname}#'.encode())
        elif signal == 2:
            self.game_name.clear()
            self.game_ppcb.setCurrentIndex(0)
            self.game_gamecb.setCurrentIndex(0)
            self.F_gamecreate.hide()


    # def test(self):
    #     self.usernum = 1
    #     self.size = [600, 800]
    #     self.sock.send(f'Gc!*!:!*!dongset!*!:!*!{self.size[0]}!*!:!*!{self.usernum}'.encode())

    def pygaming_test(self):
        pygame.init()  # 2. pygame 초기화
        self.screen = pygame.display.set_mode(self.size)

        self.done = False
        self.clock = pygame.time.Clock()

        self.runGame()

        pygame.quit()

    def runGame(self):
        dung_image = pygame.image.load('ddong.png')
        self.dung_image = pygame.transform.scale(dung_image, (50, 50))
        self.dungs = []

        character1_image = pygame.image.load('character1.png')
        self.character1_image = pygame.transform.scale(character1_image, (70, 70))
        self.character = pygame.Rect(character1_image.get_rect())
        self.character.left = self.size[0] // 2 - self.character.width // 2
        self.character.top = self.size[1] - self.character.height
        self.character_dx = 0

        character2_image = pygame.image.load('character2.png')
        self.character2_image = pygame.transform.scale(character2_image, (70, 70))
        self.character2 = pygame.Rect(character2_image.get_rect())
        self.character2.left = self.size[0] // 2 - self.character2.width // 2
        self.character2.top = self.size[1] - self.character2.height
        self.p2_dx = 0
        self.start_signal = True
        self.change = False

        for i in range(5):
            rect = pygame.Rect(self.dung_image.get_rect())
            rect.left = self.poss[i][0]
            rect.top = -100
            dy = self.poss[i][1]
            self.dungs.append({'rect': rect, 'dy': dy})

        while not self.done:
            self.screen.fill((0, 0, 0))

            if self.start_signal:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # self.done = True
                        break
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.character_dx = -10
                            msg = 'G' + '!*!:!*!' + "left" + '!*!:!*!' + 'asd'
                            time.sleep(0.001)
                            # self.sock.sendall(msg.encode())  # 클라이언트에게 내가내린명령전송
                        elif event.key == pygame.K_RIGHT:
                            self.character_dx = 10
                            msg = 'G' + '!*!:!*!' + "right" + '!*!:!*!' + 'asd'
                            time.sleep(0.001)
                            # self.sock.sendall(msg.encode())  # 클라이언트에게 내가내린명령전송
                        elif event.key == pygame.K_SPACE:
                            self.done = True
                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT:
                            self.character_dx = 0
                            msg = 'G' + '!*!:!*!' + "zero" + '!*!:!*!' + 'asd'
                            time.sleep(0.001)
                            # self.sock.sendall(msg.encode())  # 클라이언트에게 내가내린명령전송
                        elif event.key == pygame.K_RIGHT:
                            self.character_dx = 0
                            msg = 'G' + '!*!:!*!' + "zero" + '!*!:!*!' + 'asd'
                            time.sleep(0.001)
                            # self.sock.sendall(msg.encode())  # 클라이언트에게 내가내린명령전송

                for dung in self.dungs:
                    dung['rect'].top += dung['dy']
                    if dung['rect'].top > self.size[1]:
                        if self.change == False:
                            self.sock.send(f'Gc!*!:!*!redong!*!:!*!F{self.usernum}')
                        elif self.change == True:
                            self.dungs.remove(dung)
                            rect = pygame.Rect(self.dung_image.get_rect())
                            rect.left = self.rposs[0]
                            rect.top = -100
                            dy = self.rposs[1]
                            self.dungs.append({'rect': rect, 'dy': dy})

                self.character.left = self.character.left + self.character_dx
                self.character2.left = self.character2.left + self.p2_dx
                if self.character.left < 0:
                    self.character.left = 0
                elif self.character.left > self.size[0] - self.character.width:
                    self.character.left = self.size[0] - self.character.width

                self.screen.blit(self.character1_image, self.character)
                self.screen.blit(self.character2_image, self.character2)
                for dung in self.dungs:
                    if dung['rect'].colliderect(self.character):
                        self.done = False
                    self.screen.blit(self.dung_image, dung['rect'])
            else:
                pass
            self.clock.tick(40)
            pygame.display.update()

class Thread_list(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        while True:
            if self.work_relist == True:
                pass





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Cclient()
    sys.exit(app.exec_())
