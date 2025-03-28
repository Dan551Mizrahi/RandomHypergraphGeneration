from FirstMethod import generate_random_hypergraph_from_scratch
from SecondMethod import generate_random_hypergraph_from_a_tree
from writeHGtoFile import export_hg_to_dat
import random
import argparse
import os

def generate_hg_prob_p(num_hypergraphs: int,
                       p: float,
                       min_node_num: int,
                       max_node_num: int,
                       min_hyperedge_num: int,
                       max_hyperedge_num: int,
                       path: str):
    """Generates a number of random hypergraphs with a fixed probability p.
    :param num_hypergraphs: Number of hypergraphs to generate
    :param p: Probability of a node being in a hyperedge
    :param min_node_num: Minimum number of nodes in a hypergraph
    :param max_node_num: Maximum number of nodes in a hypergraph
    :param min_hyperedge_num: Minimum number of hyperedges in a hypergraph
    :param max_hyperedge_num: Maximum number of hyperedges in a hypergraph
    :param path: Path to save the .dat files"""

    for i in range(num_hypergraphs):
        num_nodes = random.randint(min_node_num, max_node_num)
        num_hyperedges = random.randint(min_hyperedge_num, max_hyperedge_num)
        num_of_he = main(1, num_nodes, num_hyperedges, p, path, name=i)
        # Save id card of the hypergraph
        with open(f'{path}/hypergraph_{i}_id.txt', 'w') as f:
            f.write(f'Number of nodes: {num_nodes}\n')
            f.write(f'Number of hyperedges: {num_of_he}\n')
            f.write(f'nodes + hyperedges: {num_nodes + num_of_he}\n')
            f.write(f'Probability p: {p:0.2f}\n')

def main(num_hypergraphs: int, num_nodes: int, num_hyperedges: int, p: float, path: str, name: str='Null'):
    """Generates a number of random hypergraphs and exports them to .dat files.
    :param num_hypergraphs: Number of hypergraphs to generate
    :param num_nodes: Number of nodes in the hypergraph
    :param num_hyperedges: Number of hyperedges in the hypergraph
    :param p: Probability of a node being in a hyperedge
    :param path: Path to save the .dat files"""
    random.seed(42)
    for i in range(num_hypergraphs):
        hypergraph = generate_random_hypergraph_from_scratch(num_nodes, num_hyperedges, p)
        if name == 'Null':
            export_hg_to_dat(hypergraph, f'{path}/hypergraph_{i}.dat')
        else:
            export_hg_to_dat(hypergraph, f'{path}/hypergraph_{name}.dat')
        return len(hypergraph)

def something():
    list_of_probabilities = [0.05*x for x in range(1, 20)]
    path = './GenDatasets'
    for p in list_of_probabilities:
        # create a folder for each probability
        os.makedirs(f'{path}/p_{p:0.2f}', exist_ok=True)
        generate_hg_prob_p(100,
                           p,
                           5,
                           50,
                           5,
                           50,
                           f'{path}/p_{p:0.2f}')
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate some number of random hypergraphs')
    parser.add_argument('num_hypergraphs', type=int, help='Number of random hypergraphs to generate')
    parser.add_argument('num_nodes', type=int, help='Number of nodes in the hypergraph')
    parser.add_argument('num_hyperedges', type=int, help='Number of hyperedges in the hypergraph')
    parser.add_argument('p', type=float, help='Probability of a node being in a hyperedge')
    parser.add_argument('path', type=str, help='Path to save the .dat files')
    args = parser.parse_args()
    main(args.num_hypergraphs, args.num_nodes, args.num_hyperedges, args.p, args.path)


