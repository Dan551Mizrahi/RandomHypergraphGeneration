import networkx as nx
import random
from collections import deque
from typing import List, Tuple, Set, Dict, Any
import matplotlib.pyplot as plt


def generate_random_hypergraph_from_a_tree(total_size: int, p: float, draw: bool = False, sperner = False) -> Set[Tuple[int, ...]]:
    """
    Generates a random connected hypergraph based on a random tree structure.

    Steps:
    1. Generate a random tree with 'total_size' nodes using networkx.
    2. Root the tree randomly and perform a BFS to create a bipartite partition
       (nodes at even levels vs. nodes at odd levels).
    3. Treat one partition as hyperedges and the other as vertices.
       Rename vertices sequentially starting from 0.
       Construct the initial hypergraph where each hyperedge (from one partition)
       contains the vertices (from the other partition) it was connected to in the tree.
    4. For each hyperedge, iterate through all *possible* vertices (0 to num_vertices-1).
       Add a vertex to the hyperedge with probability 'p' if it's not already present.
    5. Return the final hypergraph as a list of tuples, where each tuple represents
       a hyperedge and contains the integer IDs of its vertices.

    Args:
        total_size: The total number of nodes in the initial random tree.
                    This corresponds to the initial sum of vertices and hyperedges
                    before the probabilistic additions. Must be >= 1.
        p: The probability (0.0 to 1.0) of adding an existing vertex to an
           existing hyperedge (if it's not already part of it).
        draw: If True, visualize the generated tree, the partitioning,
              and the final incidence graph using matplotlib. Defaults to False.
        sperner: If True, remove the hyperedegs that are porperly contained in another hyperedge.

    Returns:
        A list of tuples. Each tuple represents a hyperedge and contains
        sorted integer IDs of the vertices belonging to that hyperedge.
        Returns an empty list if total_size is less than 1.
        Returns a list potentially containing a single hyperedge with no vertices
        if total_size is 1.

    Raises:
        ValueError: If total_size < 1 or if p is not between 0 and 1.
    """
    # --- Input Validation ---
    if total_size < 1:
         print("Warning: total_size < 1, returning empty hypergraph.")
         return [] # No nodes means no hypergraph structure

    if not (0.0 <= p <= 1.0):
        raise ValueError("Probability p must be between 0.0 and 1.0")

    # --- Step 1: Generate a Random Tree ---
    tree = nx.random_labeled_tree(total_size)

    # --- Visualization Step 1 ---
    layout = None  # Initialize layout variable
    if draw and total_size > 0:
        fig1, ax1 = plt.subplots(figsize=(8, 6))
        # Use a layout that often works well for trees
        try:
            # spring_layout can be slow for large graphs, Kamada-Kawai is often good
            layout = nx.kamada_kawai_layout(tree)
        except nx.NetworkXError:  # Fallback if Kamada-Kawai fails (e.g., disconnected, though random_tree shouldn't be)
            print("Warning: Kamada-Kawai layout failed, using spring layout.")
            layout = nx.spring_layout(tree, seed=42)  # Seed for reproducibility

        nx.draw(tree, pos=layout, with_labels=True, node_color='lightblue',
                node_size=500, font_size=10, ax=ax1)
        ax1.set_title(f"1. Initial Random Tree (Size={total_size})")
        plt.tight_layout()
        plt.show()

    if total_size == 1:
        print("Warning: total_size = 1. Resulting hypergraph may be trivial.")

    # --- Step 2: Root and Bi-partition ---
    nodes = list(tree.nodes())

    root = random.choice(nodes)

    # Perform BFS to determine levels and partition
    partition_A = set() # Nodes at even levels from root (will be hyperedges)
    partition_B = set() # Nodes at odd levels from root (will be vertices)
    level: Dict[Any, int] = {root: 0}
    queue = deque([root])
    visited: Set[Any] = {root}

    while queue:
        u = queue.popleft()
        current_level = level[u]

        # Assign node to partition based on level parity
        if current_level % 2 == 0:
            partition_A.add(u)
        else:
            partition_B.add(u)

        for v in tree.neighbors(u):
            if v not in visited:
                visited.add(v)
                level[v] = current_level + 1
                queue.append(v)

    # --- Visualization Step 2 ---
    if draw:
        fig2, ax2 = plt.subplots(figsize=(8, 6))
        node_colors = []
        color_map_viz = {'A': 'red', 'B': 'lightgreen'}  # Hyperedges red, Vertices green
        labels_viz = {}
        for node in tree.nodes():
            part = 'A' if node in partition_A else 'B'
            node_colors.append(color_map_viz[part])
            labels_viz[node] = f"{node}\n({part})"  # Label node with original ID and partition

        # Ensure layout is calculated if not done before (e.g., if total_size was 0 initially)
        if layout is None:
            layout = nx.kamada_kawai_layout(tree)

        nx.draw(tree, pos=layout, node_color=node_colors, labels=labels_viz,
                node_size=600, font_size=9, ax=ax2)
        # Highlight the root node
        nx.draw_networkx_nodes(tree, pos=layout, nodelist=[root], node_size=800,
                               node_color=color_map_viz['A' if root in partition_A else 'B'],  # Match color
                               edgecolors='black', linewidths=2.0, ax=ax2)

        ax2.set_title(f"2. Rooted Tree (Root={root}) & Bi-partition\n"
                      f"(Red={len(partition_A)} Hyperedges (A), Green={len(partition_B)} Vertices (B))")
        plt.tight_layout()
        plt.show()

    # --- Step 3: Create Initial Hypergraph ---
    vertex_nodes_original = sorted(list(partition_B)) # Sort for consistent mapping
    hyperedge_nodes_original = sorted(list(partition_A)) # Sort for potential consistency

    vertex_mapping: Dict[Any, int] = {
        orig_id: new_id for new_id, orig_id in enumerate(vertex_nodes_original)
    }
    num_vertices = len(vertex_nodes_original)
    all_renamed_vertices: Set[int] = set(range(num_vertices))

    # Map original hyperedge nodes to their corresponding initial set of (renamed) vertices
    initial_hyperedges_dict: Dict[Any, Set[int]] = {
        h_node: set() for h_node in hyperedge_nodes_original
    }

    for u, v in tree.edges():
        # Identify which node is the hyperedge (in A) and which is the vertex (in B)
        hyperedge_node_orig = None
        vertex_node_orig = None

        if u in partition_A and v in partition_B:
            hyperedge_node_orig = u
            vertex_node_orig = v
        elif v in partition_A and u in partition_B:
            hyperedge_node_orig = v
            vertex_node_orig = u
        # else: should not happen in a bipartite graph derived from a tree partition

        if hyperedge_node_orig is not None and vertex_node_orig is not None:
            renamed_vertex = vertex_mapping[vertex_node_orig]
            initial_hyperedges_dict[hyperedge_node_orig].add(renamed_vertex)

    # Get the list of initial hyperedges (as sets of vertices)
    # This automatically handles the case where a node in partition_A might have
    # had no neighbors in partition_B (though this won't happen for a connected tree > 1 node)
    initial_hyperedges_sets: List[Set[int]] = list(initial_hyperedges_dict.values())

    # Handle the total_size = 1 case explicitly here if needed
    if total_size == 1:
        pass # Logic seems to handle this, resulting in [()]

    # --- Step 4: Probabilistically Add Vertices ---
    final_hyperedges_sets: List[Set[int]] = []
    for current_hyperedge_set in initial_hyperedges_sets:
        modified_hyperedge_set = set(current_hyperedge_set) # Start with a copy

        # Consider all vertices that *could* be added
        potential_vertices_to_add = all_renamed_vertices - current_hyperedge_set

        for vertex_id in potential_vertices_to_add:
            if random.random() < p:
                modified_hyperedge_set.add(vertex_id)

        final_hyperedges_sets.append(modified_hyperedge_set)

    # --- Step 5: Format and Return ---
    # Convert sets to sorted tuples for the final output
    final_hyperedges: List[Tuple[int, ...]] = [
        tuple(sorted(list(h_set))) for h_set in final_hyperedges_sets
    ]

    # --- Visualization Step 3: Incidence Graph ---
    if draw and num_vertices > 0 and len(final_hyperedges) > 0:
        incidence_graph = nx.Graph()
        vertex_nodes_inc = list(range(num_vertices)) # Nodes 0, 1, ...
        hyperedge_nodes_inc = [f'h{i}' for i in range(len(final_hyperedges))] # Nodes h0, h1, ...

        # Add nodes with bipartite attribute
        incidence_graph.add_nodes_from(vertex_nodes_inc, bipartite=0) # Vertices are partition 0
        incidence_graph.add_nodes_from(hyperedge_nodes_inc, bipartite=1) # Hyperedges are partition 1

        # Add edges based on final hypergraph structure
        for i, h_set in enumerate(final_hyperedges_sets):
            h_node_id = f'h{i}'
            for v_id in h_set:
                if v_id in vertex_nodes_inc: # Check vertex exists
                     incidence_graph.add_edge(v_id, h_node_id)
                # else: This vertex id is invalid - shouldn't happen

        if incidence_graph.number_of_nodes() > 0:
            fig3, ax3 = plt.subplots(figsize=(8, 6))

            # Use bipartite layout
            pos_inc = nx.bipartite_layout(incidence_graph, vertex_nodes_inc, align='vertical') # Pass nodes for partition 0

            # Color nodes based on partition
            color_map_inc = []
            node_labels_inc = {}
            for node in incidence_graph.nodes():
                if incidence_graph.nodes[node]['bipartite'] == 0:
                    color_map_inc.append('lightgreen') # Vertex color
                    node_labels_inc[node] = f"v{node}" # Label as v0, v1...
                else:
                    color_map_inc.append('red') # Hyperedge color
                    node_labels_inc[node] = node # Label as h0, h1...


            nx.draw(incidence_graph, pos=pos_inc, node_color=color_map_inc, labels=node_labels_inc,
                    node_size=500, font_size=10, ax=ax3)
            ax3.set_title(f"3. Final Hypergraph Incidence Graph\n"
                          f"(Red={len(hyperedge_nodes_inc)} Hyperedges, Green={num_vertices} Vertices)")
            plt.tight_layout()
            plt.show()
        else:
             print("Skipping incidence graph plot: Graph is empty.")

    elif draw:
        print("Skipping incidence graph plot: No vertices or hyperedges in the final structure.")

    if sperner and len(final_hyperedges_sets) > 1:
        unique_hyperedges_map = {frozenset(h): h for h in final_hyperedges_sets}
        unique_hyperedges_list = list(unique_hyperedges_map.values())

        num_unique = len(unique_hyperedges_list)
        proper_subset_indices = set()

        for k in range(num_unique):
            if k in proper_subset_indices:
                continue
            h_k = unique_hyperedges_list[k]
            for j in range(num_unique):
                if k == j:
                    continue
                h_j = unique_hyperedges_list[j]

                if h_k.issubset(h_j) and h_k != h_j:
                    proper_subset_indices.add(k)
                    break

        sperner_filtered_sets = [
            unique_hyperedges_list[k]
            for k in range(num_unique) if k not in proper_subset_indices
        ]

        final_hyperedges_sets = sperner_filtered_sets

    # Convert sets to sorted tuples for the final output using the (potentially filtered) final_hyperedges_sets
    final_hyperedges: Set[Tuple[int, ...]] = {
        tuple(sorted(list(h_set))) for h_set in final_hyperedges_sets
    }

    return final_hyperedges


if __name__ == "__main__":
    size = 20 # Total nodes in the initial tree (vertices + hyperedges)
    add_prob = 0.1 # Probability to add an extra vertex to a hyperedge

    print(f"Generating hypergraph with initial size {size} and add probability {add_prob}")
    random_hg = generate_random_hypergraph_from_a_tree(size, add_prob, draw=False, sperner=True)

    print("\nGenerated Hypergraph (List of Hyperedges):")
    if not random_hg:
        print("[] (Empty Hypergraph)")
    else:
        for i, hyperedge in enumerate(random_hg):
            print(f"  Hyperedge {i}: {hyperedge}")

    print("-" * 20)