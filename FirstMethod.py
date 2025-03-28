import random

def generate_random_hypergraph_from_scratch(num_nodes: int, num_hyperedges: int, p: float, make_simple: bool=True, make_connected: bool=True):
    """Generates a random hypergraph.
    :param num_nodes: Number of nodes in the hypergraph
    :param num_hyperedges: Number of hyperedges in the hypergraph
    :param p: Probability of a node being in a hyperedge
    :param make_simple: If True, the hypergraph will be simple (no hyperedge is a subset of another), but it may be smaller than num_hyperedges.
    :param make_connected: If True, the hypergraph will be connected, but it may be smaller than num_hyperedges, we will take its biggest connected component.
    :return: dict"""
    hypergraph = []
    nodes_list = range(num_nodes)
    for i in range(num_hyperedges):
        hypergraph.append([])
        for node in nodes_list:
            if random.random() < p:
                hypergraph[i].append(node)
    indices_to_remove = set()
    for i, hyperedge in enumerate(hypergraph):
        if len(hyperedge) == 0:
            indices_to_remove.add(i)
    for i in sorted(indices_to_remove, reverse=True):
            hypergraph.pop(i)

    # Make sure that the hypergraph is connected
    if make_connected:
        connected_components = []
        visited = set()
        for i in range(len(hypergraph)):
            if i not in visited:
                component = set()
                stack = [i]
                while stack:
                    node = stack.pop()
                    if node not in visited:
                        visited.add(node)
                        component.add(node)
                        for j in range(len(hypergraph)):
                            if j not in visited and (set(hypergraph[node]) & set(hypergraph[j])):
                                stack.append(j)
                connected_components.append(component)
        largest_component = max(connected_components, key=len)
        hypergraph = [hypergraph[i] for i in largest_component]
    # Make sure that the hypergraph is simple
    if make_simple:
        indices_to_remove = set()
        for i in range(len(hypergraph)):
            for j in range(i+1, len(hypergraph)):
                if set(hypergraph[i]).issubset(hypergraph[j]):
                    indices_to_remove.add(i)
                    break
                elif set(hypergraph[j]).issubset(hypergraph[i]):
                    indices_to_remove.add(j)
        for i in sorted(indices_to_remove, reverse=True):
            hypergraph.pop(i)

    return set(map(tuple, hypergraph))




