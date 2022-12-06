from scipy.sparse.linalg import svds
from scipy.sparse import csc_matrix, csr_matrix, bmat, eye, coo_matrix
from scipy.sparse import random, block_diag, diags
from networkx.algorithms import bipartite
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from heapq import nlargest
plt.rcParams['figure.figsize'] = [12, 8]
plt.rcParams['figure.dpi'] = 100


def to_graph(A):
    return bipartite.matrix.from_biadjacency_matrix(A)

def gcc(graph):
    return graph.subgraph(max(nx.connected_components(graph), key=len))

def top_bottom(graph):
    top_nodes = {n for n, d in graph.nodes(data=True) if d["bipartite"] == 0}
    bottom_nodes = set(graph) - top_nodes
    return top_nodes, bottom_nodes

def largest_hubs(graph, k=0.2):
    top, bottom = top_bottom(graph)
    m_top = max(1, int(len(top) * k))
    m_bot = max(1, int(len(bottom) * k))
    degree = lambda x: graph.degree[x]
    top_largest = nlargest(m_top, top, key=degree)
    bottom_largest = nlargest(m_bot, bottom, key=degree)
    return top_largest, bottom_largest

def reduce(graph, k=0.2):
    top_largest, bottom_largest = largest_hubs(graph, k)
    graph.remove_nodes_from(top_largest + bottom_largest)
    new_graph = gcc(graph).copy()
    graph.remove_nodes_from(new_graph.nodes())
    # print(len(graph), len(new_graph), len(top_largest + bottom_largest))
    return (*top_bottom(graph), new_graph, top_largest, bottom_largest)

# def fastpi(G, P1, P2, size, k=0.2):
def fastpi(A, P1, P2, k=0.2):
    print('Starting FPI...')
    data = np.zeros(shape=(len(P1), len(P2)))
    for i in range(len(P1)):        
        vals = A[i]
        for j in range(len(vals)):
            data[i][j] =1    
    A2 = coo_matrix(data)
    graph = to_graph(A2)
    top, bottom = top_bottom(graph)


    m_top = max(1, int(len(top) * k))
    m_bot = max(1, int(len(bottom) * k))
    nt = []
    nb = []
    perm_top_lhs = []
    perm_top_rhs = []
    perm_bot_lhs = []
    perm_bot_rhs = []
    
    while m_top < len(top) and m_bot < len(bottom):
        m_top = max(1, int(len(top) * k))
        m_bot = max(1, int(len(bottom) * k))
        ptl, pbl, graph, ptr, pbr = reduce(graph, k)
        perm_top_lhs = perm_top_lhs + list(ptl)
        perm_bot_lhs = perm_bot_lhs + list(pbl)
        perm_top_rhs = list(ptr) + perm_top_rhs
        perm_bot_rhs = list(pbr) + perm_bot_rhs
        nt.append(len(perm_top_lhs))
        nb.append(len(perm_bot_lhs))
        top, bottom = top_bottom(graph)
        
    perm_top = np.array(perm_top_lhs + list(top) + perm_top_rhs)

    n_perm_top =[]
    for i in perm_top:
        n_perm_top.append(P1[i])

    perm_bot = np.array(perm_bot_lhs + list(bottom) + perm_bot_rhs) - A2.shape[0]
    
    n_perm_bot=[]
    for i in perm_bot:
        n_perm_bot.append(P2[i])
    

    return n_perm_top + n_perm_bot

