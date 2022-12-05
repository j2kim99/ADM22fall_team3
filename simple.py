import numpy as np

def degsort(G):
    deg = []
    for v in G:
        deg.append(len(v))
    deg = np.array(deg)
    return deg.argsort()[::-1]

def BFS(G):
    chk = [False for _ in range(len(G))]
    rtn = []
    while not all(chk):
        s = 0
        q = []
        while chk[s]:
            s += 1
        q.append(s)
        chk[s] = True
        while len(q)>0:
            v = q.pop(0)
            rtn.append(v)
            for u in G[v]:
                if not chk[u]:
                    q.append(u)
                    chk[u] = True
    return rtn

def SO(G, hash_num = 5):
    V = len(G)
    fingerprints = np.zeros((V, hash_num))
    for k in range(hash_num):
        perm = np.random.permutation(V)
        for v in range(V):
            fingerprints[v][k] = perm[min(G[v], key=lambda x: perm[x])]
    tupleprints = [tuple(f) for f in fingerprints]
    return sorted(range(len(tupleprints)), key=tupleprints.__getitem__)

def bipartite_degsort(G, partA, partB):
    return sorted(partA, reverse=True, key=lambda x: len(G[x]))+\
        sorted(partB, reverse=True, key=lambda x: len(G[x]))

def bipartite_SO(G, partA, partB, hash_num=5):
    V = len(G)
    fingerprints = np.zeros((V, hash_num))
    for k in range(hash_num):
        perm = np.random.permutation(V)
        for v in range(V):
            fingerprints[v][k] = perm[min(G[v], key=lambda x: perm[x])]
    tupleprints = [tuple(f) for f in fingerprints]
    return sorted(partA, key=tupleprints.__getitem__)+\
        sorted(partB, key=tupleprints.__getitem__)

def random_perm(G):
    V = len(G)
    return np.random.permutation(V)

def bipartite_random(G, partA, partB):
    V1 = len(partA)
    V2 = len(partB)
    P1 = np.random.permutation(V1)
    P2 = np.random.permutation(V2)+V1

    return np.concatenate((P1, P2))