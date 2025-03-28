import random
from main import main
import os

def generate_hg_prob_p(num_hypergraphs: int,
                       p: float,
                       min_node_num: int,
                       max_node_num: int,
                       min_hyperedge_num: int,
                       max_hyperedge_num: int,
                       path: str,
                       method: str='from_scratch'):
    """Generates a number of random hypergraphs with a fixed probability p.
    :param num_hypergraphs: Number of hypergraphs to generate
    :param p: Probability of a node being in a hyperedge
    :param min_node_num: Minimum number of nodes in a hypergraph
    :param max_node_num: Maximum number of nodes in a hypergraph
    :param min_hyperedge_num: Minimum number of hyperedges in a hypergraph
    :param max_hyperedge_num: Maximum number of hyperedges in a hypergraph
    :param path: Path to save the .dat files
    :param method: Method to generate the hypergraph (from_scratch or from_tree)"""

    for i in range(num_hypergraphs):
        num_nodes = random.randint(min_node_num, max_node_num)
        num_hyperedges = random.randint(min_hyperedge_num, max_hyperedge_num)
        main(1, num_nodes, num_hyperedges, p, path, method=method, name=f"{i}_nodes_{num_nodes}_hyperedges_{num_hyperedges}_p_{p:.2f}_{method}")

def create_diverse_dataset(method: str='from_scratch'):
    list_of_probabilities = [0.05*x for x in range(1, 20)]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(script_dir, 'GenDatasets')
    os.makedirs(path, exist_ok=True)
    for p in list_of_probabilities:
        # create a folder for each probability
        os.makedirs(f'{path}/p_{p:0.2f}', exist_ok=True)
        generate_hg_prob_p(100,
                           p,
                           5,
                           50,
                           5,
                           50,
                           f'{path}/p_{p:0.2f}',
                           method=method)

if __name__ == '__main__':
    create_diverse_dataset('from_tree')