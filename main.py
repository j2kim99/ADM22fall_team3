import numpy as np
import click
from util import *

from simple import *

@click.command()
@click.option('--data', type=str, default='minigraph')
@click.option('--method', type=str, default='degsort')
@click.option('--size', type=int, default=2)
@click.option('--dbg', type=bool, default=False)
def main(data, method, size, dbg):
    path = f'data/{data}/'
    G = read_graph(path+'adjlist.txt')
    V, E, P1, P2 = read_meta(path+'metadata.txt')

    if method == 'degsort':
        perm = degsort(G)
    elif method == 'BFS':
        perm = BFS(G)

    blks = count_blocks(G, perm, size)
    if dbg:
        print(perm)
    print(blks)
    if dbg:
        print_adjmat(G, perm, size)



if __name__ == '__main__':
    main()
