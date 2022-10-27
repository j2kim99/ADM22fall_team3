import numpy as np
import random

def set_seed(seed):
    np.random.seed(seed)
    random.seed(seed)
    # torch.manual_seed(seed)

def read_graph(path):
    f = open(path, 'r')
    lines = f.readlines()
    graph = []
    for i, l in enumerate(lines):
        tokens = l.split()
        graph.append([])
        for t in tokens:
            graph[i].append(int(t))
    f.close()
    return graph

def read_meta(path):
    f = open(path, 'r')
    lines = f.readlines()
    V = int(lines[0].split()[1])
    E = int(lines[1].split()[1])
    P1 = [int(v) for v in lines[2].split()[1:]]
    P2 = [int(v) for v in lines[3].split()[1:]]
    return V, E, P1, P2

def count_blocks(graph, inv_perm, size):
    V = len(inv_perm)
    perm = list(range(V))
    for i in range(V):
        perm[inv_perm[i]] = i
    B = (V+1)//size
    chk = np.zeros((B, B))
    for i, l in enumerate(graph):
        v = perm[i]
        bv = v//size
        for u in l:
            chk[bv][perm[u]//size] = 1
    return int(sum(sum(chk)))

def print_adjmat(graph, inv_perm, size):
    V = len(inv_perm)
    perm = list(range(V))
    for i in range(V):
        perm[inv_perm[i]] = i
    newG = [[] for _ in range(V)]
    for i in range(V):
        v = perm[i]
        for j in graph[i]:
            u = perm[j]
            newG[v].append(u)
    for i in range(V):
        if i%size == 0:
            print()
        str = ''
        for j in range(V):
            if j%size == 0:
                str += ' '
            if j in newG[i]:
                str += '1 '
            else:
                str += '0 '
        print(str)
        