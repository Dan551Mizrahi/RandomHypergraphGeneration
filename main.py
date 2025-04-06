from FirstMethod import generate_random_hypergraph_from_scratch
from SecondMethod import generate_random_hypergraph_from_a_tree
from writeHGtoFile import export_hg_to_dat
import random
import argparse
import os

def main(num_hypergraphs: int, num_nodes: int, num_hyperedges: int, p: float, path: str, method: str, name: str='Null'):
    """Generates a number of random hypergraphs and exports them to .dat files.
    :param num_hypergraphs: Number of hypergraphs to generate
    :param num_nodes: Number of nodes in the hypergraph
    :param num_hyperedges: Number of hyperedges in the hypergraph
    :param p: Probability of a node being in a hyperedge
    :param path: Path to save the .dat files
    :param method: Method to generate the hypergraph (from_scratch or from_tree)
    :param name: Name of the hypergraph (for saving purposes)
    """
    for i in range(num_hypergraphs):
        if method == 'from_scratch':
            hypergraph = generate_random_hypergraph_from_scratch(num_nodes, num_hyperedges, p)
        else:
            hypergraph = generate_random_hypergraph_from_a_tree(num_nodes + num_hyperedges, p, sperner=True)
        if name == 'Null':
            export_hg_to_dat(hypergraph, f'{path}/hypergraph_{i}.dat')
        else:
            export_hg_to_dat(hypergraph, f'{path}/hypergraph_{name}.dat')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate some number of random hypergraphs')
    parser.add_argument('num_hypergraphs', type=int, help='Number of random hypergraphs to generate')
    parser.add_argument('num_nodes', type=int, help='Number of nodes in the hypergraph')
    parser.add_argument('num_hyperedges', type=int, help='Number of hyperedges in the hypergraph')
    parser.add_argument('p', type=float, help='Probability of a node being in a hyperedge')
    parser.add_argument('path', type=str, help='Path to save the .dat files')
    parser.add_argument('--method', type=str, choices=['from_scratch', 'from_tree'], default='from_scratch', help='Method to generate the hypergraph (default: from_scratch)')
    args = parser.parse_args()
    main(args.num_hypergraphs, args.num_nodes, args.num_hyperedges, args.p, args.path, args.method)


