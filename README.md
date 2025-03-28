# Random Hypergraph Generation

This project provides tools to generate random hypergraphs using different methodologies and export them to `.dat` files. It also includes functionality to create datasets of hypergraphs with varying parameters.

## Features

* **Two Generation Methods:**
    * **`from_scratch` (`FirstMethod.py`)**: Generates hypergraphs by randomly assigning vertices to a specified number of hyperedges based on a probability `p`. It includes options to enforce simplicity (no hyperedge is a subset of another) and connectivity (by taking the largest connected component). Note that enforcing these constraints might result in fewer hyperedges than initially requested.
    * **`from_tree` (`SecondMethod.py`)**: Generates a connected hypergraph based on a random tree. It partitions the tree nodes into two sets (vertices and hyperedges) and then probabilistically adds extra vertices to the hyperedges based on probability `p`. Includes an option for visualizing the generation steps.
* **Dataset Creation (`createDataset.py`)**: Script to automatically generate a structured dataset of hypergraphs, varying the generation probability `p` across a specified range. Saves results into organized folders.
* **Flexible Output (`writeHGtoFile.py`, `main.py`)**: Generated hypergraphs are saved in a simple `.dat` format, with options for custom naming.

## Dependencies

* Python 3.x
* `networkx` (required for the `from_tree` method)
* `matplotlib` (optional, only required if using the `draw=True` feature in `SecondMethod.py`)
* `scipy`

You can typically install the required libraries using pip:
```bash
pip install networkx matplotlib scipy
```

## File Structure
```
RandomHypergraphGeneration/
├── main.py                 - Main script for generating hypergraphs via CLI
├── FirstMethod.py          - Implements the "from_scratch" generation method
├── SecondMethod.py         - Implements the "from_tree" generation method
├── writeHGtoFile.py        - Utility function to write hypergraphs to .dat files
├── createDataset.py        - Script to generate datasets with varying parameters
└── README.md               - This file
```

## Usage

### Generating Single/Multiple Hypergraphs (<code>main.py</code>)

You can generate hypergraphs using the command line interface provided by <code>main.py</code>.

#### Arguments:
* <code>num_hypergraphs</code>: Number of hypergraphs to generate.
* <code>num_nodes</code>: Number of vertices in the hypergraph.
* <code>num_hyperedges</code>: Number of hyperedges in the hypergraph (initial number for <code>from_scratch</code>).
* <code>p</code>: Probability of adding a vertex to a hyperedge.
* <code>--method</code>: Generation method to use. Options are:
    * <code>from_scratch</code>: Generates hypergraphs from scratch (default).
    * <code>from_tree</code>: Generates hypergraphs based on a random tree.

#### Example Command:
```bash
python3 main.py 10 50 20 0.1 /path/to/output --method from_tree
```
This command generates 10 hypergraphs using the <code>from_tree</code> method. 
For this method, <code>num_nodes</code> (50) and <code>num_hyperedges</code> (20) are added to define the initial tree size (70). The probability <code>p</code> is 0.1, and files will be saved in <code>/path/to/output</code>.

### Generating Datasets (<code>createDataset.py</code>)
To generate a larger dataset with varying probabilities, you can run the <code>createDataset.py</code> script.
```bash
python3 createDataset.py
```
This script currently generates 100 hypergraphs for each probability <code>p</code> from 0.05 to 0.95 (in steps of 0.05), using the <code>from_tree</code> method with node and hyperedge counts randomly chosen between 5 and 50. The output is saved into subdirectories within <code>GenDatasets/</code> named according to the probability (e.g., <code>GenDatasets/p_0.10/</code>). You can modify the parameters and method directly within the <code>createDataset.py</code> script.

## Output Format (<code>.dat</code> files)
Generated hypergraphs are saved in `.dat` files. Each line in the file represents a single hyperedge, consisting of space-separated integer IDs of the vertices belonging to that hyperedge.
```
0 5 12
1 5 8 9
0 2 10
...
```

This indicates three hyperedges: {0, 5, 12}, {1, 5, 8, 9}, and {0, 2, 10}.

## AI Usage Acknowledgment

Parts of this project were developed with the assistance of AI tools. Specifically:
* **Google Gemini:** Utilized for generating code structures, explaining algorithms, debugging, and drafting documentation (including portions of this README).
* **GitHub Copilot:** Employed for code completion and suggestions during the development process.
