from socket import *
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import threading
from PyQt5 import QtCore, QtWidgets
import pymysql
import datetime
import json
#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("livechat.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget_2.setCurrentIndex(0)
        self.initialize_socket()
        self.btn_send.clicked.connect(self.send_chat)   #메시지 송신 버튼누르면 송신됨
        self.btn_enter.clicked.connect(self.go_chat)   #채팅방 들어가는 버튼
        self.btn_back.clicked.connect(self.go_home) #뒤로가기버튼
        self.btn_create.clicked.connect(self.room_create)
        self.tableWidget.cellDoubleClicked.connect(self.go_roomchat)
        self.go_chat_list = []
        self.go_roomchat_list =[]
        self.go_new_list = []
        self.go_now_list=[]

    def receive_message(self, so):
        while True:
            buf=so.recv(8192).decode('utf-8')
            if not buf:
                break
            recv_data=buf
            if '@' in recv_data:    #대화방명 불러오기
                recv_roomname_remove=recv_data.replace('@', '')
                recv_roomname = json.loads(recv_roomname_remove)
                for i in range(len(recv_roomname)):
                    self.go_chat_list.append(recv_roomname[i][0])
                self.tableWidget.setRowCount(len(self.go_chat_list))
                self.tableWidget.setColumnCount(1)
                for i in range(len(self.go_chat_list)):
                    self.tableWidget.setItem(0, i, QTableWidgetItem(self.go_chat_list[i]))
            if '!' in recv_data:    #지난 채팅불러오기
                recv_dia_remove=recv_data.replace('!', '')
                self.go_roomchat_list = json.loads(recv_dia_remove)
                for i in range(len(self.go_roomchat_list)):
                    self.listWidget.insertItem(i, f'{self.go_roomchat_list[i][0]} : {self.go_roomchat_list[i][2]}')
                self.listWidget.addItem(f'{self.name_edit.text()}님 입장하셨습니다.')
            if '*' in recv_data:    #대화방추가
                recv_new_remove = recv_data.replace('*', '')
                self.go_new_list = json.loads(recv_new_remove)
                self.tableWidget.insertRow(1)
                self.tableWidget.setColumnCount(1)
                if self.room_name_create.text() not in self.go_chat_list:   #대화방명 중복안되게
                    for i in range(len(self.go_new_list)):
                        self.tableWidget.setItem(i, 0, QTableWidgetItem(str(self.go_new_list[i][0])))
            if '@' or '!' or '*' not in recv_data:
                print("dasfdsafsdaf")
                # self.go_now_list = json.loads(recv_data)
                # print(self.go_now_list)

        so.close()

    def send_chat(self):    #송신 메시지 창에서 메시지를 읽어 수신메시지  창에 표시하고 전송
        time = datetime.datetime.now().strftime("%Y/%m/%d  %H:%M:%S")
        chat_list=[]    # [이름,채팅방명,메시지,날짜]
        chat_list.append(self.name_edit2.text())
        chat_list.append(self.room_name.text())
        chat_list.append(self.msg_edit.text())
        chat_list.append(time)
        self.client_socket.send(json.dumps(chat_list).encode('utf-8'))
        # message = json.dumps(f'{chat_list}%').encode('utf-8')  # 송신메시지 인코딩
        # self.client_socket.send(message)

        # # self.listWidget.addItem(f"{self.name_edit.text()} : {data}")  #송신메시지 텍스트브라우저에 띄우기
        # # message=(f'{self.name_edit.text()} : {data}').encode('utf8')    #송신메시지 인코딩

        # self.msg_edit.clear()

    def go_roomchat(self):
        message = json.dumps(f'{self.tableWidget.currentItem().text()}!').encode('utf-8')  # 송신메시지 인코딩
        self.client_socket.send(message)
        self.listWidget.clear()
        self.stackedWidget_2.setCurrentIndex(1)
        self.room_name.setText(self.tableWidget.currentItem().text())

    def room_create(self):
        print("대화방만들기버튼누르면 추가됨~~")
        message = json.dumps(f'{self.room_name_create.text()}*').encode('utf-8')  # 송신메시지 인코딩
        self.client_socket.send(message)
        if self.room_name_create.text() in self.go_chat_list:
            QtWidgets.QMessageBox.information(self, "QMessageBox", "이미 있는 방명입니다.")

    def go_home(self):  #뒤로가기버튼
        self.stackedWidget.setCurrentIndex(0)


    def go_chat(self):
        self.name_edit2.setText(self.name_edit.text())
        message = json.dumps('@').encode('utf-8')  # 송신메시지 인코딩
        self.client_socket.send(message)
        self.stackedWidget.setCurrentIndex(1)

    def initialize_socket(self):    #tcp socket을 생성하고 server와 연결함
        self.client_socket=socket(AF_INET, SOCK_STREAM)
        ip = '10.10.21.109'
        port = 9000
        self.client_socket.connect((ip, port))

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()
    myWindow.setWindowTitle("채팅프로그램")
    #프로그램 화면을 보여주는 코드
    myWindow.show()
    cThread=threading.Thread(target=myWindow.receive_message, args=(myWindow.client_socket,))
    cThread.start()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()