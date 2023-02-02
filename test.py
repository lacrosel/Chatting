from datetime import datetime

import pymysql
from datetime import datetime
from dateutil.relativedelta import relativedelta
#
# info = {'1': ['qqq', 'www', 'eee'], '2': ['two', 'three']}
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

db = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r',
                                             charset='utf8')
cursor = db.cursor()
check = cursor.execute(f"SELECT sender, msg "
                       f"FROM chatserver.mainchat "
                       f"WHERE dates LIKE '2023-02%' ORDER BY dates DESC, times DESC")
chatlog = cursor.fetchall()
db.close()

# print(chatlog)
now = datetime.now()
check = now - relativedelta(months=0)
print(check.strftime('%Y-%m'))

