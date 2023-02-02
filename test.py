info = {'1': ['qqq', 'www', 'eee'], '2': ['two', 'three']}
rinfo = {'1': ['빙고', '4인'], '2': ['빙고', '2인']}

roomname = list(info.keys())
print(roomname)
kk = []
for name in roomname:
    ll = rinfo[name]
    kk.append([name, ll[0], ll[1][0], str(len(info[name]))])
print(kk)