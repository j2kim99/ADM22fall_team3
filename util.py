import numpy as np
import random
from scipy.sparse import coo_matrix
from collections import defaultdict
from scipy.sparse import csr_matrix

import pickle

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
    B = 1+(V-1)//size
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

def save_mat(G, inv_perm, path):
    V = len(inv_perm)
    perm = list(range(V))
    for i in range(V):
        perm[inv_perm[i]] = i
    rows = []
    cols = []
    vals = []
    for i in range(V):
        v = perm[i]
        for j in G[i]:
            u = perm[j]
            rows.append(v)
            cols.append(u)
            vals.append(1)
    rows = np.array(rows)
    cosl = np.array(cols)
    vals = np.array(vals)
    mat = csr_matrix((vals, (rows, cols)), shape=(V, V))
    with open(path, 'wb') as f:
        pickle.dump(mat, f)


def arrange_bipartite(graph, partA, partB):
    b0 = len(partA)
    A = {a:i for i, a in enumerate(partA)}
    B = {b:(i+b0) for i, b in enumerate(partB)}
    G = [[] for _ in range(len(partA)+len(partB))]
    for va in partA:
        v = A[va]
        for ub in graph[va]:
            G[v].append(B[ub])
    for vb in partB:
        v = B[vb]
        for ua in graph[vb]:
            G[v].append(A[ua])
    return G, list(range(len(partA))), list(range(len(partA), len(partA)+len(partB)))


def scc(nodes=[], edges=[]):
    """
    A function that computes strongly connected components using Kosaraju's algorithm. Returns list of components, which are list of nodes.

    Args:
        nodes (list): List of nodes of any type.
        edges (list): List of edges, where each edge is a pair of nodes (ex: (0, 1)).

    Returns:
        List of strongly connected components. Each component is just a list of nodes.
    """
    alists = defaultdict(lambda: [])
    rlists = defaultdict(lambda: [])
    avisited = defaultdict(lambda: False)
    rvisited = defaultdict(lambda: False)
    leader = defaultdict(lambda: None)
    components = defaultdict(lambda: [])
    f = {}
    r = {}
    nodes = nodes
    edges = edges
    n = len(nodes)
    for u, v in edges:
        alists[u].append(v)
        rlists[v].append(u)
    t = 0
    for s in nodes:
        if rvisited[s]:
            continue
        rvisited[s] = True
        stack = [s]
        while len(stack):
            i = stack[-1]
            sink = True
            for j in rlists[i]:
                if not rvisited[j]:
                    rvisited[j] = True
                    stack.append(j)
                    sink = False
                    break
            if sink:
                t += 1
                f[i] = t
                stack.pop()
    for key in f:
        r[f[key]] = key
    for t in range(n, 0, -1):
        s = r[t]
        if avisited[s]:
            continue
        avisited[s] = True
        stack = [s]
        while len(stack):
            i = stack.pop()
            leader[i] = s
            components[s].append(i)
            for j in alists[i]:
                if not avisited[j]:
                    avisited[j] = True
                    stack.append(j)
    return [components[leader] for leader in components]

def preprocess(V,G):
    rows = []
    cols = []
    vals = []
    for v in range(V):
        for u in G[v]:
            rows.append(v)
            cols.append(u)
            vals.append(1)
    mat = csr_matrix((vals, (rows, cols)), shape=(V, V))
    data=coo_matrix(mat)
    return data
