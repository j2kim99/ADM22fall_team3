import numpy as np
import click
from util import *

from fastpi import *
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
    if method.casefold() == 'degsort'.casefold() or method.casefold() == 'deg'.casefold():
        perm = degsort(G)
    if method.casefold() == 'bideg'.casefold():
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

        
    elif method.casefold() == 'IBSO'.casefold():
        perm = IBSO(G, P1, P2, size)
        
    elif method.casefold() =='fp'.casefold() or method.casefold()=='fastpi'.casefold():
        cooG=preprocess(V,G)
        perm = fastpi(cooG)

    if dbg:
        print('lenperm:', len(perm))
    blks = count_blocks(G, perm, size)
    print("nonzero blocks:", blks)
    
    if showmat:
        print_adjmat(G, perm, size)



if __name__ == '__main__':
    main()
