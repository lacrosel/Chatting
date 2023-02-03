from socket import *
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from threading import *
import pymysql
import datetime
import json
import datetime



class multichatserver:
    def __init__(self):
        self.clients = []  # 접속된 클라이언트 소켓 목록
        self.final_received_message = []  # 최종 수신 메시지
        self.s_sock = socket(AF_INET, SOCK_STREAM)
        self.ip = '10.10.21.109'
        self.port = 9000
        self.s_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.s_sock.bind((self.ip, self.port))
        print("클라이언트 대기중..")
        self.s_sock.listen(5)  # 연결대기
        self.accept_client()
        self.go_chat_list = []
        self.go_roomchat_list =[]
        self.go_roomchat_name=[]
        self.new_room_list=[]

    # 연결 클라이언트 소켓을 목록에 추가하고 스레드를 생성하여 데이터를 수신한다
    def accept_client(self):
        while True:
            client = c_socket, (ip, port) = self.s_sock.accept()
            if client not in self.clients:
                self.clients.append(client)  # 접속된 소켓을 목록에 추가
            print(ip, ':', str(port), '가 연결되었습니다.')
            print(self.clients)
            print(len(self.clients))
            cth = Thread(target=self.receive_messages, args=(c_socket,))  # 수신스레드
            cth.start()  # 스레드시작

    # 데이터를 수신하여 모든 클라이언트에게 전송한다
    def receive_messages(self, c_socket):
        while True:
            try:
                incoming_message = json.loads(c_socket.recv(8192).decode('utf-8'))  # [이름,채팅방명,메시지,날짜]
                print(f"실시간1{incoming_message}")
                if not incoming_message:  # 연결이 종료됨
                    break
            except:
                continue
            else:
                if '@' in incoming_message:
                    self.go_chat_list = incoming_message
                    self.go_chat(c_socket)
                if '!' in incoming_message:
                    self.go_roomchat_name = incoming_message
                    self.go_roomchat(c_socket)
                if '*' in incoming_message:
                    self.new_roomchat_name = incoming_message
                    self.room_create(c_socket)
                if '@' or '!' or '*' not in incoming_message:
                    self.final_received_message = incoming_message
                    self.send_all_clients(c_socket)

    def send_all_clients(self, senders_socket):
        conn = pymysql.connect(host="localhost", user="root", password="1234", db="livechat",
                               charset="utf8")
        curs = conn.cursor()

        # print(self.final_received_message)
        # AB=self.final_received_message
        # result = ','.join(str(s) for s in AB)
        # print(result)
        # print(type(result))
        # b=result.split(',')
        # print(b)
        # print(type(b))
        # print(b[1])
        print(self.final_received_message)
        print(type(self.final_received_message))
        print(self.final_received_message[0])
        # print(self.final_received_message[1][0])
        # print(a[1])
        # print(a[0][1])
        # print(self.final_received_message[3])
        # print(type(self.final_received_message))
        # print(len(self.final_received_message))
        # print(type(self.final_received_message[0]))
        print(type(self.final_received_message[1:2]))
        a=self.final_received_message[2:3]
        # print(a[0])
        # print(self.final_received_message[3:4][0])
        # print(self.final_received_message[1][0])
        # curs.execute(f"insert into live_chat (chat_name,chat_room_name,chat_room_detail,chat_time) values ('{self.final_received_message[0]}','{self.final_received_message[1:2]}','{self.final_received_message[2:3]}','{self.final_received_message[3:4]}')")
        # conn.commit()
        # for client in self.clients:  # 목록에 있는 모든 소켓에 대해
        #     socket, (ip, port) = client
        #     if socket is not senders_socket:  # 송신 클라이언트는 제외
        #         try:
        #             socket.sendall(json.dumps(self.final_received_message).encode('utf-8'))
        #         except:  # 연결종료
        #             self.clients.remove(client)  # 소켓제거
        #             print(f"{ip},{port},연결이 종료되었습니다.")

    def room_create(self, senders_socket):
        print("1111")
        recv_new_remove = self.new_roomchat_name.replace('*', '')
        conn = pymysql.connect(host="localhost", user="root", password="1234", db="livechat", charset="utf8")
        curs = conn.cursor()
        time=datetime.datetime.now()
        # self.new_room_list = []
        curs.execute(f"insert into live_chat (chat_room_name) values ('{recv_new_remove}')")
        conn.commit()
        curs.execute(f"select distinct chat_room_name from live_chat")
        roomname_rows = curs.fetchall()
        for client in self.clients:  # 목록에 있는 모든 소켓에 대해
            socket, (ip, port) = client
            # if socket is not senders_socket:  # 송신 클라이언트는 제외
            try:
                a = json.dumps(roomname_rows)
                b = a + "*"
                socket.sendall(b.encode('utf-8'))
            except:  # 연결종료
                self.clients.remove(client)  # 소켓제거
                print(f"{ip},{port},연결이 종료되었습니다.")
    def go_roomchat(self, senders_socket):
        recv_roomname_remove = self.go_roomchat_name.replace('!', '')
        conn = pymysql.connect(host="localhost", user="root", password="1234", db="livechat", charset="utf8")
        curs = conn.cursor()
        time=datetime.datetime.now()
        curs.execute(f"select * from live_chat where chat_room_name='{recv_roomname_remove}' order by chat_time desc  LIMIT 10")
        rows = curs.fetchall()
        print(f"채팅내용{rows}")
        for client in self.clients:  # 목록에 있는 모든 소켓에 대해
            socket, (ip, port) = client
            # if socket is not senders_socket:  # 송신 클라이언트는 제외
            try:
                a = json.dumps(rows)
                b = a + "!"
                socket.sendall(b.encode('utf-8'))
            except:  # 연결종료
                self.clients.remove(client)  # 소켓제거
                print(f"{ip},{port},연결이 종료되었습니다.")

    def go_chat(self, senders_socket):
        print("sdaf")
        conn = pymysql.connect(host="localhost", user="root", password="1234", db="livechat", charset="utf8")
        curs = conn.cursor()
        curs.execute(f"select distinct chat_room_name from live_chat")
        name_rows = curs.fetchall()
        print(f"db에서뺀거 {name_rows}")
        # self.go_chat_list.append(name_rows)
        for client in self.clients:  # 목록에 있는 모든 소켓에 대해
            socket, (ip, port) = client
            # if socket is not senders_socket:  # 송신 클라이언트는 제외
            try:
                a = json.dumps(name_rows)
                b = a + "@"
                socket.sendall(b.encode('utf-8'))
            except:  # 연결종료
                self.clients.remove(client)  # 소켓제거
                print(f"{ip},{port},연결이 종료되었습니다.")

    # 송신 클라이언트를 제외한 모든 클라이언트에게 메시지 전송




if __name__ == "__main__":
    multichatserver()