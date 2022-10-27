import numpy as np

def degsort(G):
    deg = []
    for v in G:
        deg.append(len(v))
    deg = np.array(deg)
    return deg.argsort()[::-1]

def BFS(G, start = 0):
    chk = [False for _ in range(len(G))]
    rtn = []
    q = [start]
    chk[start] = True
    while len(q)>0:
        v = q.pop(0)
        rtn.append(v)
        for u in G[v]:
            if not chk[u]:
                q.append(u)
                chk[u] = True
    return rtn
