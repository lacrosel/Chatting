from datetime import datetime

import pymysql
from datetime import datetime
from dateutil.relativedelta import relativedelta
# #
# userlist = ['qqq','www','eee','two','three']
# info = {'1': ['qqq', 'www', 'eee'], '2': ['two', 'three']}
# for i in info:
#     print(i)
#
#
# for user in userlist:
#     for roomname in info:
#         if user in info[roomname]:
#             temp = user + ' - ' + roomname
#             print(temp)


# rinfo = {'1': ['빙고', '4인'], '2': ['빙고', '2인']}
#
# roomname = list(info.keys())
# print(roomname)
# kk = []
# for name in roomname:
#     ll = rinfo[name]
#     kk.append([name, ll[0], ll[1][0], str(len(info[name]))])
# print(kk)
#
# now= datetime.now()
# print(now)
# print(now.strftime('%H:%M:%S'))
# print(now.strftime('%Y-%m-%d'))
#
# a=now.strftime('%H:%M:%S')
#
# print(a)
#
# db = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r',
#                                              charset='utf8')
# cursor = db.cursor()
# check = cursor.execute(f"SELECT sender, msg "
#                        f"FROM chatserver.mainchat "
#                        f"WHERE dates LIKE '2023-02%' ORDER BY dates DESC, times DESC")
# chatlog = cursor.fetchall()
# db.close()
#
# # print(chatlog)
# now = datetime.now()
# check = now - relativedelta(months=0)
# print(check.strftime('%Y-%m'))
#
import random

# rannum = [1, 2, 3, 4, 5]
# # random.shuffle(rannum)
# for i in range(1, 22):
#     i=i%len(rannum)
# #     print(rannum[-i])
# n= '이'
# u = ['정', '강', '이']
#
# t = u.index('3')
# print(t)
# t = (t+1)%len(u)
# print(u[t])
# rinfo = {'1': ['빙고', '4인'], '2': ['빙고', '2인']}
#
# if '빙고' not in rinfo:
#     print("222")


JDnum = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
indx = [[1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20],
        [21, 22, 23, 24, 25]]
pick = [1, 2, 3, 4, 5]


