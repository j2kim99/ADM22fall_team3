# Iterative Bucket Shingle Ordering

import numpy as np

def BSO(G, permA, partB, size, hash_num=5):
    blk_num = 1+(len(permA)-1)//size
    inv_permA = {v:i for i, v in enumerate(permA)}

    fingerprints = np.zeros((len(partB), hash_num))
    for iter in range(hash_num):
        blk_perm = np.random.permutation(blk_num)
        for i, v in enumerate(partB):
            minu = min(G[v], key=lambda u: blk_perm[inv_permA[u]//size])
            fingerprints[i][iter] = blk_perm[inv_permA[minu]//size]
    tupleprints = [tuple(f) for f in fingerprints]
    permB = sorted(range(len(tupleprints)), key=tupleprints.__getitem__)

    return [partB[i] for i in permB]


def IBSO(G, partA, partB, size, hash_num=5, iter = 3):
    permA = partA
    permB = partB

    for _ in range(iter):
        # print(permA, permB)
        permB = BSO(G, permA, permB, size, hash_num)
        # print('permB', permB)
        permA = BSO(G, permB, permA, size, hash_num)
        # print('permA', permA)

    return permA+permB