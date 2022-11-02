import numpy as np
import click
from util import *

from simple import *
from IBSO import *
from slashburn import *

@click.command()
@click.option('--data', type=str, default='minibipartite')
@click.option('--method', type=str, default='degsort')
@click.option('--size', type=int, default=2)
@click.option('--dbg', type=bool, default=False)
@click.option('--showmat', type=bool, default=False)
@click.option('--seed', type=int, default=0)
def main(data, method, size, dbg, showmat, seed):
    path = f'data/{data}/'
    G = read_graph(path+'adjlist.txt')
    V, E, P1, P2 = read_meta(path+'metadata.txt')

    G, P1, P2 = arrange_bipartite(G, P1, P2)
    if showmat:
        print_adjmat(G, list(range(V)), size)

    if dbg:
        print(f'V:{V}, P1:{len(P1)}, P2:{len(P2)}, E:{E}')

    set_seed(seed)
    if method == 'degsort':
        perm = degsort(G)
    elif method == 'BFS':
        perm = BFS(G)
    elif method == 'SO' or method == 'shingle':
        perm = SO(G)
    elif method =='SB' or method=='slashburn':
        perm=SB(G)
    elif method == 'IBSO':
        perm = IBSO(G, P1, P2, size)
    
    if dbg:
        # print(perm)
        print('lenperm:', len(perm))
    blks = count_blocks(G, perm, size)
    print("nonzero blocks:", blks)
    if showmat:
        print_adjmat(G, perm, size)



if __name__ == '__main__':
    main()
