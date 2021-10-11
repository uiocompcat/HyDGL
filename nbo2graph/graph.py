import torch
from datetime import datetime
from torch_geometric.data import Data

from nbo2graph.file_handler import FileHandler
from nbo2graph.element_look_up_table import ElementLookUpTable


class Graph:

    """Class for reading relevant data from QM output files."""

    def __init__(self, nodes, edges, attributes=[], graph_features=[]):

        """Constructor

        Args:
            nodes (list[list[floats]]): List of node feature vectors.
            edges (list[list[int], list[float]]): List with individual sublists for connected node indices as well as edge features.
            attributes (list[float]): List of attributes/labels associated to graph (e.g. HOMO-LUMO gap).
            graph_features (list): List of graph level features.
        """

        self.nodes = nodes
        self.edges = edges
        self.attributes = attributes
        self.graph_features = graph_features

    def get_pytorch_data_object(self) -> Data:

        """Generates a pytorch data object ready to use for learning/visualisation.

        Returns:
            torch_geometric.data.Data: Pytorch data object containing nodes, edges and edge features.
        """

        # set up pytorch object for edges
        # include reverse edges (to account for both directions)
        edge_indices = torch.tensor([x[0] for x in self.edges] + [list(reversed(x[0])) for x in self.edges], dtype=torch.long)
        # set up pytorch object for edge features
        # duplicated list to account for the attributes of the additional reverse edges
        edge_features = torch.tensor([x[1] for x in self.edges * 2], dtype=torch.float)

        # set up pytorch object for nodes
        node_features = torch.tensor(self.nodes, dtype=torch.float)

        # set up full pytorch data object
        data = Data(x=node_features, edge_index=edge_indices.t().contiguous(), edge_attr=edge_features)

        return data

    def write_mol_file(self, file_path: str):

        """Writes the graph in mol format to file.

        Args:
            filepath (string): The path to the output file.
        """

        # data to write
        data = 'Molecule\n_generated ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n\n'

        # set up summary data line
        data += str(len(self.nodes)).rjust(3, ' ') + str(len(self.edges)).rjust(3, ' ') + '  0  0  0  0  0  0  0  0999 V2000\n'

        # TODO node resolve relies on the fact the the first element of each feature string contains the atomic number
        for i in range(len(self.nodes)):
            data += '    0.0000    0.0000    0.0000 ' + ElementLookUpTable.get_element_identifier(self.nodes[i][0]).ljust(5, ' ') + '0  0  0  0  0  0  0  0  0  0  0  0\n'

        # bond order is read out from first position in edge feature vector
        for i in range(len(self.edges)):

            bond_order = 1
            if self.edges[i][1][0] > 1.5:
                bond_order = 2
            if self.edges[i][1][0] > 2.5:
                bond_order = 3

            data += str(self.edges[i][0][0] + 1).rjust(3, ' ') + str(self.edges[i][0][1] + 1).rjust(3, ' ') + str(bond_order).rjust(3, ' ') + '  0  0  0  0 \n'

        data += 'M  END'
        FileHandler.write_file(file_path, data)

    def is_connected(self) -> bool:

        """Determines whether there are not connected nodes.

        Returns:
            bool: Boolean to describe whether the graph is connected or not.
        """

        # if there is exactly one (disjoint) subgraph then the graph is connected
        if len(self.get_disjoint_sub_graphs()) == 1:
            return True

        # otherwise there are not connected --> disconnected
        return False

    def get_disjoint_sub_graphs(self) -> list[list[int]]:

        """Gets a list of lists of node indices belonging to respective disjoint subgraphs.

        Returns:
            list[list[int]]: List of subgraph node indices.
        """

        # output list
        disjoint_sub_graphs = []
        # contains all node indices
        not_visited_nodes = list(range(len(self.nodes)))

        while len(not_visited_nodes) > 0:

            # list to store the nodes part of the current (disjoint) sub graph
            current_sub_graph_indices = []
            # set up new queue with first element of not yet visited nodes
            node_queue = [not_visited_nodes[0]]

            while len(node_queue) > 0:

                # get neighbours of current node
                neighbours = self.get_adjacent_nodes(node_queue[0])
                # dequeue
                current_sub_graph_indices.append(node_queue[0])
                node_queue.pop(0)
                # enqueue (only enque nodes that have not been visited before and are not already in queue)
                node_queue.extend(list(set(neighbours) - set(current_sub_graph_indices) - set(node_queue)))

            # update list of not visited nodes
            not_visited_nodes = list(set(not_visited_nodes) - set(current_sub_graph_indices))

            # append subgraph to output list
            disjoint_sub_graphs.append(current_sub_graph_indices)

        # return disjoint sub graphs as sub lists
        return disjoint_sub_graphs

    def get_adjacent_nodes(self, node_index: int) -> list[int]:

        """Gets the indices of adjacent (neighbour by one edge) nodes of a given node based on the edge data.

        Raises:
            ValueError: If the specified node is out of the valid range (either less than zero or higher than the number of nodes).

        Returns:
            list[int]: List of node indices denoting the adjacent nodes.
        """

        if node_index < 0 or node_index > len(self.nodes) - 1:
            raise ValueError('The specified node index is out of range. Valid range: 0 - ' + str(len(self.nodes) - 1) + '. Given: ' + str(node_index) + '.')

        adjacent_nodes = []
        for i in range(len(self.edges)):
            if node_index in self.edges[i][0]:
                # get the index of the other node in the edge node list
                other_edge_index = (self.edges[i][0].index(node_index) + 1) % 2
                # get the appropriate node index
                adjacent_node_index = self.edges[i][0][other_edge_index]
                # append to output list
                adjacent_nodes.append(adjacent_node_index)

        return adjacent_nodes
