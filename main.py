import numpy as np
import click
from time import time
from util import *

from simple import *
from IBSO import *
from slashburn import *
from fastpi import *

@click.command()
@click.option('--data', type=str, default='minibipartite')
@click.option('--method', type=str, default='random')
@click.option('--size', type=int, default=2)
@click.option('--dbg', type=bool, default=False)
@click.option('--showmat', type=bool, default=False)
@click.option('--seed', type=int, default=0)
@click.option('--save', type=str, default='')
def main(data, method, size, dbg, showmat, seed, save):
    path = f'data/{data}/'
    G = read_graph(path+'adjlist.txt')
    V, E, P1, P2 = read_meta(path+'metadata.txt')

    G, P1, P2 = arrange_bipartite(G, P1, P2)
    if showmat:
        print_adjmat(G, list(range(V)), size)

    if dbg:
        print(f'V:{V}, P1:{len(P1)}, P2:{len(P2)}, E:{E}')
    #print(G)
    set_seed(seed)
    start_time = time()
    if method.casefold() == 'random'.casefold() or method.casefold() == 'rand'.casefold():
        perm = random_perm(G)
    elif method.casefold() == 'bipartite_random'.casefold() or method.casefold() == 'birand'.casefold():
        perm = bipartite_random(G, P1, P2)
    elif method.casefold() == 'degsort'.casefold() or method.casefold() == 'deg'.casefold():
        perm = degsort(G)
    elif method.casefold() == 'bideg'.casefold():
        perm = bipartite_degsort(G, P1, P2)
    elif method.casefold() == 'BFS'.casefold():
        perm = BFS(G)
    elif method.casefold() == 'SO'.casefold() or method.casefold() == 'shingle'.casefold():
        perm = SO(G)
    elif method.casefold() == 'biSO'.casefold() or method.casefold() == 'bishingle'.casefold():
        perm = bipartite_SO(G, P1, P2)
    elif method.casefold() =='SB'.casefold() or method.casefold()=='slashburn'.casefold():
        cooG=preprocess(V,G)
        perm =slashburn(cooG)
    elif method.casefold() =='fp'.casefold() or method.casefold()=='fastpi'.casefold():
        perm = fastpi(G, P1, P2)
    elif method.casefold() == 'IBSO'.casefold():
        perm = IBSO(G, P1, P2, size)
    elapsed_time = time()-start_time
    if dbg:
        print('lenperm:', len(perm))
    blks = count_blocks(G, perm, size)
    print("nonzero blocks:", blks)
    print(f"elapsed time: {elapsed_time:.4f} sec")
    if showmat:
        print_adjmat(G, perm, size)
    if save != '':
        save_mat(G, perm, save)



if __name__ == '__main__':
    main()
