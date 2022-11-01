import numpy as np
import click
from util import *

from simple import *
from IBSO import *

@click.command()
@click.option('--data', type=str, default='minibipartite')
@click.option('--method', type=str, default='degsort')
@click.option('--size', type=int, default=2)
@click.option('--dbg', type=bool, default=False)
@click.option('--seed', type=int, default=0)
def main(data, method, size, dbg, seed):
    path = f'data/{data}/'
    G = read_graph(path+'adjlist.txt')
    V, E, P1, P2 = read_meta(path+'metadata.txt')

    G, P1, P2 = arrange_bipartite(G, P1, P2)
    if dbg:
        print_adjmat(G, list(range(V)), size)

    set_seed(seed)

    if method == 'degsort':
        perm = degsort(G)
    elif method == 'BFS':
        perm = BFS(G)
    elif method == 'SO' or method == 'shingle':
        perm = SO(G)
    elif method == 'IBSO':
        perm = IBSO(G, P1, P2, size)

    blks = count_blocks(G, perm, size)
    if dbg:
        print(perm)
    print("nonzero blocks:", blks)
    if dbg:
        print_adjmat(G, perm, size)



if __name__ == '__main__':
    main()
