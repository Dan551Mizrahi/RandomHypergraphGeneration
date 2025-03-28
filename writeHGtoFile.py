
def export_hg_to_dat(hypergraph: set, path: str):
    """Exports a hypergraph to a .dat file.
    :param hypergraph: Hypergraph to export
    :param path: Path to save the .dat file"""
    with open(path, 'w') as f:
        for vertices in hypergraph:
            f.write(" ".join(map(str, vertices)))
            f.write('\n')

