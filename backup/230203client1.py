import socket
import sys
import time
import threading
import pyautogui
from PyQt5 import uic
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import *
from datetime import datetime
from dateutil.relativedelta import relativedelta
# import pygame
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
        self.logSignal = 0
        self.now = datetime.now()
        self.F_gamecreate.hide()
        self.F_gameinvite.hide()
        self.F_alert.hide()
        self.alert_close.clicked.connect(lambda: self.F_alert.hide())

        self.listWidget.doubleClicked.connect(lambda: self.chatLog(0, 0))
        self.gr_roomclose.clicked.connect(lambda: self.pageReset(1))
        self.create_cancel.clicked.connect(lambda: self.pageReset(2))
        self.create_agree.clicked.connect(self.gameRoom_create)
        self.CHAT_gamecreate.clicked.connect(self.gameCreate_check)
        self.CHAT_gameEnter.clicked.connect(lambda: self.gameRoom_Enter(0, 0))
        self.game_renewal.clicked.connect(lambda: self.inviteList_renewal(0))
        self.CHAT_renewal.clicked.connect(self.mainPage_renewal)
        self.gr_sendbt.clicked.connect(lambda: self.gameRoomChat(0))
        self.gr_sendtext.returnPressed.connect(lambda: self.gameRoomChat(0))

        self.Game_userlist2.doubleClicked.connect(lambda: self.userinvite(0, 0))
        self.game_initebt.clicked.connect(lambda: self.userinvite(0, 0))
        self.invite_yes.clicked.connect(lambda: self.userinvite(2, 0))
        self.invite_no.clicked.connect(lambda: self.userinvite(3, 0))

        self.connection.clicked.connect(self.admission)
        self.CHAT_BT_tsend.clicked.connect(self.sendMsg)
        self.CHAT_LE_tsend.returnPressed.connect(self.sendMsg)
        self.CHAT_timeExit.clicked.connect(self.CHAT_exit)

        # self.CHAT_game.clicked.connect(self.test)

    def chatLog(self, signal, data):
        if signal == 0:
            if self.listWidget.currentRow() == 0:
                self.logSignal += 1
                self.listWidget.insertItem(0, '=========================================')  # 맨 앞에 추가하기.
                # logsignal횟수-1만큼 현재 달에서 빼준 달의 데이터 요청할 것.

                check = self.now - relativedelta(months=self.logSignal - 1)
                print(check.strftime('%Y-%m-%d'))
                msg = 'C!*!:!*!' + str(check.strftime('%Y-%m-%d')) + 'L'
                self.sock.send(msg.encode())
        elif signal == 1:
            check = self.now - relativedelta(months=0)
            check = check.strftime('%Y-%m')
            if check == data[1]:
                self.listWidget.clear()

            for row in range(len(data[0])):
                self.listWidget.insertItem(0, f'[{data[0][row][0]}] {data[0][row][1]}')  # 맨 앞에 추가하기.
            self.listWidget.insertItem(0, f'@@  {data[1]}  메세지 @@')  # 맨 앞에 추가하기.

    def userinvite(self, signal, data):
        if signal == 0:
            try:
                toUser = self.Game_userlist2.item(self.Game_userlist2.currentRow(), 0).text()
                print(toUser, ' 초대')
                msg = 'Gr!*!:!*!' + self.name + '!@#' + toUser + '!*!:!*!' + self.gr_roomname.text() + '^%^' + self.gr_gamename.text() + 'I'
                self.sock.send(msg.encode())
            except AttributeError:
                return
        elif signal == 1:
            # sender+'!@#'+recver+'!@#' + msg
            info = data.split('!@#')
            print(info)
            # 방이름 , 게임종류
            self.info2 = info[2].split('^%^')
            print(self.info2)
            self.F_gameinvite.show()
            self.invite_text.setPlainText(f"{info[0]}님이\n{self.info2[0]}-{self.info2[1]}\n초대했습니다.")

        elif signal == 2:  # 수락
            self.F_gameinvite.hide()
            self.sock.send(f'Gr!*!:!*!{self.name}!*!:!*!{self.info2[0]}$'.encode())

        elif signal == 3:  # 거절
            # self.invite_text.clear()
            self.F_gameinvite.hide()

    def admission(self):  # 서버 접속
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

    def mainList_set(self, ulist):  # 메인 유저 리스트와 게임방 리스트 데이터 출력
        # 메인 유저리스트
        self.CHAT_userlist.clearContents()
        self.CHAT_userlist.setRowCount(len(ulist[0]))
        self.CHAT_userlist.setColumnCount(len(ulist[0][0]))
        for row in range(len(ulist[0])):
            self.CHAT_userlist.setItem(row, 0, QTableWidgetItem(ulist[0][row][0]))  # 닉네임
            self.CHAT_userlist.setItem(row, 1, QTableWidgetItem(ulist[0][row][1]))  # 위치

        # 메인 게임방 리스트
        self.CHAT_gamerlist.clearContents()
        if len(ulist[1]) > 0:
            self.CHAT_gamerlist.setRowCount(len(ulist[1]))
            for row in range(len(ulist[1])):
                self.CHAT_gamerlist.setItem(row, 0, QTableWidgetItem(str(ulist[1][row][0])))
                self.CHAT_gamerlist.setItem(row, 1, QTableWidgetItem(str(ulist[1][row][1])))
                self.CHAT_gamerlist.setItem(row, 2,
                                            QTableWidgetItem(str(ulist[1][row][3]) + ' / ' + str(ulist[1][row][2])))

    def sendMsg(self):  # 채팅 msg 보내기
        message = 'C' + '!*!:!*!' + self.CHAT_LE_tsend.text() + 'C'
        if self.CHAT_LE_tsend.text() == "" or self.CHAT_LE_tsend.text() is None:
            return
        self.sock.send(message.encode())
        self.CHAT_LE_tsend.clear()

    def recvMsg(self, sock):  # 신호 받기 메서드 원래는 채팅뿐이었지만 다른 기능들 모두
        while True:
            data = sock.recv(1024)  # 서버로부터 문자열 수신
            if not data:  # 문자열 없으면 종료
                break
            print(data.decode())
            msg = data.decode().split('!*!:!*!')
            print(msg)
            if msg[0] == 'X':
                if msg[1] == 'X':
                    self.alert_text.setText('이미 존재하는 닉네임입니다.')
                    self.F_alert.show()
                    self.running = False
                    break
                elif msg[1] == 'O':
                    self.CHAT_STACK.setCurrentIndex(1)
            if msg[0] == 'C':  # 일반 채팅 식별문자
                if msg[1][-1] == 'C':
                    self.listWidget.addItem(msg[1][:-1])
                    self.scollcheck(0)
                elif msg[1][-1] == 'L':
                    chatlogdata = json.loads(msg[1][:-1])
                    self.chatLog(1, chatlogdata)
            # if msg[0] == 'G':
            #     print(msg)
            #     if msg[1] == 'right':
            #         self.p2_dx = 10
            #     elif msg[1] == 'left':
            #         self.p2_dx = -10
            #     elif msg[1] == 'zero':
            #         self.p2_dx = 0
            # if msg[0] == 'Gc':
            #     print("동데이터!")
            #     if msg[1] == 'dongset':
            #         self.poss = json.loads(msg[2])
            #         print(self.poss)
            #         self.pygaming_test()
            #     elif msg[1] == 'redong':
            #         print('동이다')
            #         self.rposs = json.loads(msg[2])
            if msg[0] == 'Gr':  # 게임방 식별 문자
                if msg[1][-1] == '!':  # 게임방 생성 불가
                    self.alert_text.setText('이미 존재하는 방입니다.')
                    self.F_alert.show()
                elif msg[1][-1] == '@':  # 게임방 생성 승인
                    self.gru_list = json.loads(msg[1][:-1])
                    self.gameroomset(1)
                elif msg[1][-1] == '^':  # 게임방 입장 승인
                    self.gru_list = json.loads(msg[1][:-1])
                    self.gameRoom_Enter(1, self.gru_list)
                    self.inviteList_renewal(1)
                elif msg[1][-1] == '*':  # 게임방 입장 거절
                    self.alert_text.setText('해당 방의 정원이 초과했습니다.')
                    self.F_alert.show()

                elif msg[1][-1] == '%':  # 게임방 내 데이터 갱신
                    self.gru_list = json.loads(msg[1][:-1])
                    self.inviteList_renewal(1)
                elif msg[1][-1] == 'C':  # 일반 게임챗
                    self.gr_chat.addItem(msg[1][:-1])
                    self.scollcheck(1)
                elif msg[1][-1] == 'I':  # 게임 초대
                    # 'Gr!*!:!*!'+sender+'!@#'+recver+'!@#' + msg
                    print('초대받음')
                    self.userinvite(1, msg[1][:-1])

            if msg[0] == 'L':  # 메인 채팅 페이지 갱신 식별
                if msg[1][-1] == 'C':
                    print('제이슨!')
                    ulist = json.loads(msg[1][:-1])  # bytes형으로 수신된 데이터를 문자열로 변환 출력 json.loads
                    print('ulist',ulist)
                    self.mainList_set(ulist)

            # except Exception as e:  # 어떤 에러 일지 모르니까 표시만 하고 서버 멈추지는 않도록 처리.
            #     print(e)
            if not self.running:
                break
        self.sock.close()
        print("중지")

    def mainPage_renewal(self):  # 메인페이지 갱신 요청
        msg = 'L!*!:!*!' + 'C'
        self.sock.send(msg.encode())

    def gameCreate_check(self):  # 방만들기 hide 상태의 프레임 show해서 프레임 내의 위젯들 보여주기
        self.F_gamecreate.show()

    def gameroomset(self, signal):  # 방 생성 허락 후 방 기본값 셋팅
        if signal == 1:
            self.CHAT_STACK.setCurrentIndex(2)  # 이동
            print(len(self.gru_list[0]))
            print(len(self.gru_list[1]))
            self.gr_roomname.setText(self.game_name.text())
            self.gr_people.setText(self.game_ppcb.currentText())
            self.gr_gamename.setText(self.game_gamecb.currentText())
            self.pageReset(2)
            # 게임방 접속 인원
            self.Game_userlist.clearContents()
            self.Game_userlist.setRowCount(len(self.gru_list[0]))
            self.Game_userlist.setColumnCount(1)
            # 초대 가능 인원
            self.Game_userlist2.clearContents()  # 초기화
            self.Game_userlist2.setRowCount(len(self.gru_list[1]))
            self.Game_userlist2.setColumnCount(1)

            for ii in range(len(self.gru_list[0])):  # 접속 인원 출력
                self.Game_userlist.setItem(ii, 0, QTableWidgetItem(self.gru_list[0][ii]))
            for oo in range(len(self.gru_list[1])):  # 접속 인원 출력
                self.Game_userlist2.setItem(oo, 0, QTableWidgetItem(self.gru_list[1][oo]))

    def gameRoomChat(self, signal):
        if signal == 0:
            roomname = self.gr_roomname.text()
            message = 'Gr' + '!*!:!*!' + roomname + '%@%' + self.name + '!*!:!*!' + self.gr_sendtext.text() + 'C'
            if self.gr_sendtext.text() == "" or self.gr_sendtext.text() is None:
                return
            self.sock.send(message.encode())
            self.gr_sendtext.clear()

    def scollcheck(self, signal):
        time.sleep(0.005)
        if signal == 0:
            self.listWidget.scrollToBottom()
        elif signal == 1:
            self.gr_chat.scrollToBottom()

    def CHAT_exit(self):  # 메인채팅 퇴장
        self.running = False
        message = 'C' + '!*!:!*!' + 'E!X@I#T%C'
        print("asd")
        self.sock.send(message.encode())
        time.sleep(1)
        self.listWidget.clear()
        self.CHAT_STACK.setCurrentIndex(3)

    def gameRoom_create(self):  # 게임방 만들기 요청
        if self.game_name.text() is None or self.game_ppcb.currentIndex() == 0 or self.game_gamecb.currentIndex() == 0:
            a = QMessageBox.information(self, "알림", "정보를 확인 해주세요.")
            return
        roomInfo = [self.game_name.text(), self.game_gamecb.currentText(), self.game_ppcb.currentText()]
        sendInfo = json.dumps(roomInfo)  # 방 정보 json변환
        self.sock.send(f'Gr!*!:!*!{self.name}!*!:!*!{sendInfo}@'.encode())

    def gameRoom_Enter(self, signal, roominfo):  # 게임방 입장 요청
        try:
            if signal == 0:  # 입장 요청
                roomname = self.CHAT_gamerlist.item(self.CHAT_gamerlist.currentRow(), 0).text()
                self.sock.send(f'Gr!*!:!*!{self.name}!*!:!*!{roomname}$'.encode())
            elif signal == 1:  # 승인
                self.gr_roomname.setText(roominfo[1][0])
                self.gr_gamename.setText(roominfo[1][1])
                self.gr_people.setText(roominfo[1][2])
                self.CHAT_STACK.setCurrentIndex(2)  # 이동
        except AttributeError:
            a = QMessageBox.information(self, "알림", "방을 선택해주세요")
            return

    def inviteList_renewal(self, signal):  # 게임방 내 초대가능 유저 리스트 갱신 및 요청
        if signal == 0:  # 시그널이 0일땐 요청
            self.sock.send(f'Gr!*!:!*!{self.name}!*!:!*!{self.gr_roomname.text()}%'.encode())
        elif signal == 1:  # 시그널이 1일땐 데이터 갱신
            self.Game_userlist.clearContents()
            self.Game_userlist.setRowCount(len(self.gru_list[0][0]))
            for ii in range(len(self.gru_list[0][0])):  # 접속 인원 출력
                self.Game_userlist.setItem(ii, 0, QTableWidgetItem(self.gru_list[0][0][ii]))
            # 초대 가능 인원
            self.Game_userlist2.clearContents()  # 초기화
            if len(self.gru_list[0][1]) > 0:
                self.Game_userlist2.setRowCount(len(self.gru_list[0][1]))
                for oo in range(len(self.gru_list[0][1])):  # 접속 인원 출력
                    self.Game_userlist2.setItem(oo, 0, QTableWidgetItem(self.gru_list[0][1][oo]))

    def pageReset(self, signal):
        if signal == 1:  # 게임방에서 나갔을때. 초기화
            # self.Game_userlist2.clear()
            # self.Game_userlist.clear()
            # self.gr_chat.clear()
            # self.gr_sendtext.clear()
            self.CHAT_STACK.setCurrentIndex(1)
            self.sock.send(f'Gr!*!:!*!{self.name}!*!:!*!{self.gr_roomname.text()}#'.encode())
        elif signal == 2:  # 게임방 입장시 초기화
            self.game_name.clear()
            self.game_ppcb.setCurrentIndex(0)
            self.game_gamecb.setCurrentIndex(0)
            self.F_gamecreate.hide()

    # def test(self):
    #     self.usernum = 1
    #     self.size = [600, 800]
    #     self.sock.send(f'Gc!*!:!*!dongset!*!:!*!{self.size[0]}!*!:!*!{self.usernum}'.encode())


#
#     def pygaming_test(self):
#         pygame.init()  # 2. pygame 초기화
#         self.screen = pygame.display.set_mode(self.size)
#
#         self.done = False
#         self.clock = pygame.time.Clock()
#
#         self.runGame()
#
#         pygame.quit()
#
#     def runGame(self):
#         dung_image = pygame.image.load('ddong.png')
#         self.dung_image = pygame.transform.scale(dung_image, (50, 50))
#         self.dungs = []
#
#         character1_image = pygame.image.load('character1.png')
#         self.character1_image = pygame.transform.scale(character1_image, (70, 70))
#         self.character = pygame.Rect(character1_image.get_rect())
#         self.character.left = self.size[0] // 2 - self.character.width // 2
#         self.character.top = self.size[1] - self.character.height
#         self.character_dx = 0
#
#         character2_image = pygame.image.load('character2.png')
#         self.character2_image = pygame.transform.scale(character2_image, (70, 70))
#         self.character2 = pygame.Rect(character2_image.get_rect())
#         self.character2.left = self.size[0] // 2 - self.character2.width // 2
#         self.character2.top = self.size[1] - self.character2.height
#         self.p2_dx = 0
#         self.start_signal = True
#         self.change = False
#
#         for i in range(5):
#             rect = pygame.Rect(self.dung_image.get_rect())
#             rect.left = self.poss[i][0]
#             rect.top = -100
#             dy = self.poss[i][1]
#             self.dungs.append({'rect': rect, 'dy': dy})
#
#         while not self.done:
#             self.screen.fill((0, 0, 0))
#
#             if self.start_signal:
#                 for event in pygame.event.get():
#                     if event.type == pygame.QUIT:
#                         # self.done = True
#                         break
#                     elif event.type == pygame.KEYDOWN:
#                         if event.key == pygame.K_LEFT:
#                             self.character_dx = -10
#                             msg = 'G' + '!*!:!*!' + "left" + '!*!:!*!' + 'asd'
#                             time.sleep(0.001)
#                             # self.sock.sendall(msg.encode())  # 클라이언트에게 내가내린명령전송
#                         elif event.key == pygame.K_RIGHT:
#                             self.character_dx = 10
#                             msg = 'G' + '!*!:!*!' + "right" + '!*!:!*!' + 'asd'
#                             time.sleep(0.001)
#                             # self.sock.sendall(msg.encode())  # 클라이언트에게 내가내린명령전송
#                         elif event.key == pygame.K_SPACE:
#                             self.done = True
#                     elif event.type == pygame.KEYUP:
#                         if event.key == pygame.K_LEFT:
#                             self.character_dx = 0
#                             msg = 'G' + '!*!:!*!' + "zero" + '!*!:!*!' + 'asd'
#                             time.sleep(0.001)
#                             # self.sock.sendall(msg.encode())  # 클라이언트에게 내가내린명령전송
#                         elif event.key == pygame.K_RIGHT:
#                             self.character_dx = 0
#                             msg = 'G' + '!*!:!*!' + "zero" + '!*!:!*!' + 'asd'
#                             time.sleep(0.001)
#                             # self.sock.sendall(msg.encode())  # 클라이언트에게 내가내린명령전송
#
#                 for dung in self.dungs:
#                     dung['rect'].top += dung['dy']
#                     if dung['rect'].top > self.size[1]:
#                         if self.change == False:
#                             self.sock.send(f'Gc!*!:!*!redong!*!:!*!F{self.usernum}')
#                         elif self.change == True:
#                             self.dungs.remove(dung)
#                             rect = pygame.Rect(self.dung_image.get_rect())
#                             rect.left = self.rposs[0]
#                             rect.top = -100
#                             dy = self.rposs[1]
#                             self.dungs.append({'rect': rect, 'dy': dy})
#
#                 self.character.left = self.character.left + self.character_dx
#                 self.character2.left = self.character2.left + self.p2_dx
#                 if self.character.left < 0:
#                     self.character.left = 0
#                 elif self.character.left > self.size[0] - self.character.width:
#                     self.character.left = self.size[0] - self.character.width
#
#                 self.screen.blit(self.character1_image, self.character)
#                 self.screen.blit(self.character2_image, self.character2)
#                 for dung in self.dungs:
#                     if dung['rect'].colliderect(self.character):
#                         self.done = False
#                     self.screen.blit(self.dung_image, dung['rect'])
#             else:
#                 pass
#             self.clock.tick(40)
#             pygame.display.update()
#
#
# class Thread_list(QThread):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.parent = parent
#
#     def run(self):
#         while True:
#             if self.work_relist == True:
#                 pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Cclient()
    sys.exit(app.exec_())
