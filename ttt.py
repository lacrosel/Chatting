

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

#
JDnum = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

arr = []
count=0
for i in range(5):
    aa= []
    for j in range(5):
        aa.append(JDnum[count])
        count += 1
    arr.append(aa)

print(arr)





# indx = [[1, 2, 3, 4, 5],
#      [6, 7, 8, 9, 10],
#      [11, 12, 13, 14, 15],
#      [16, 17, 18, 19, 20],
#      [21, 22, 23, 24, 25]]
# pick = [1, 2, 3, 4, 5, 14,18,7,9,22,25,11,17,6,16,21]
#
# checker = 0
# for i in pick:
#     if i not in JDnum:
#         checker +=1
#
# if checker != 0:
#     print("불일치")
# if pick in JDnum:
#     print('11')
#
#
#
# total = []
#
# for row in range(5):
#     da = []
#     for col in range(5):
#         da.append(indx[row][col])
#     total.append(da)
# for row in range(5):
#     da = []
#     for col in range(5):
#         da.append(indx[col][row])
#     total.append(da)
# aa=[]
# bb=[]
# for row in range(5):
#     j = 4-row
#     aa.append(indx[row][j])
#     bb.append(indx[row][row])
# total.append(aa)
# total.append(bb)
# # print(total)
# count = 0
# bingo = 0
# for arr in total:
#     count += 1
#     print(count)
#     checker = 0
#     for ck in arr:
#         if ck not in pick:
#             checker += 1
#     if checker == 0:
#         bingo += 1
#         print('빙고')

