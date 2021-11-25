import torch
# from datetime import datetime
import plotly.graph_objects as go
from torch_geometric.data import Data

# from nbo2graph.file_handler import FileHandler
from nbo2graph.element_look_up_table import ElementLookUpTable


class Graph:

    """Class for representing chemical graphs with all necessary information."""

    def __init__(self, nodes, edges, targets=[], graph_features=[], id=None, stoichiometry=None):

        """Constructor

        Args:
            id (string): Identifier inferred from the file name.
            stoichiometry (string): Stoichiometry of the molecule.
            labels (list[string]): List of labels for visualisation.
            positions (list[list[float]]): List of 3d lists of float xyz positions for visualisation.
            nodes (list[list[floats]]): List of node feature vectors.
            edges (list[list[int], list[float]]): List with individual sublists for connected node indices as well as edge features.
            targets (list[float]): List of targets/labels associated to graph (e.g. HOMO-LUMO gap).
            graph_features (list): List of graph level features.
        """

        self._id = id
        self._stoichiometry = stoichiometry

        self._nodes = nodes
        self._edges = edges
        self._targets = targets
        self._graph_features = graph_features

    def __str__(self):

        out = 'Graph Info:\n\n'
        out += f'ID: {self.id}\nStoichiometry: {self.stoichiometry}\n\n'
        out += f'Number of nodes: {len(self.nodes)}\n'
        out += f'Number of edges: {len(self.edges)}\n\n'

        out += f'Number of node features: {len(self.nodes[0])}\n'
        out += f'Number of edge features: {len(self.edges[0][1])}\n'
        out += f'Number of graph features: {len(self.graph_features)}\n'
        out += f'Number of targets: {len(self.targets)}\nIs connected: {self.is_connected()}\n\n'

        out += f'Nodes:\n{self.nodes}\n\n'
        out += f'Edges:\n{self.edges}\n\n'
        out += f'Graph features:\n{self.graph_features}\n\n'
        out += f'Graph targets:\n{self.targets}\n\n'

        return out

    @property
    def id(self):
        """Getter for id."""
        return self._id

    @property
    def stoichiometry(self):
        """Getter for stoichiometry."""
        return self._stoichiometry

    @property
    def nodes(self):
        """Getter for nodes."""
        return self._nodes

    @property
    def edges(self):
        """Getter for edges."""
        return self._edges

    @property
    def targets(self):
        """Getter for targets."""
        return self._targets

    @property
    def graph_features(self):
        """Getter for graph_features."""
        return self._graph_features

    @property
    def nodes_features_list(self):
        """Getter for a list of node features."""
        return [x.features for x in self._nodes]

    @property
    def nodes_labels_list(self):
        """Getter for a list of node labels."""
        return [x.label for x in self._nodes]

    @property
    def edges_indices_list(self):
        """Getter for a list of edge indices."""
        return [x.node_indices for x in self._edges]

    @property
    def edges_features_list(self):
        """Getter for a list of edge features."""
        return [x.features for x in self._edges]

    def get_pytorch_data_object(self) -> Data:

        """Generates a pytorch data object ready to use for learning/visualisation.

        Returns:
            torch_geometric.data.Data: Pytorch data object containing nodes, edges and edge features.
        """

        # set up pytorch object for edges
        # include reverse edges (to account for both directions)
        edge_indices = torch.tensor(self.edges_indices_list + [list(reversed(x)) for x in self.edges_indices_list], dtype=torch.long)
        # set up pytorch object for edge features
        # duplicated list to account for the targets of the additional reverse edges
        edge_features = torch.tensor(self.edges_features_list * 2, dtype=torch.float)

        # set up pytorch object for nodes
        node_features = torch.tensor(self.nodes_features_list, dtype=torch.float)

        # set up pytorch object for graph level targets / labels
        targets = torch.tensor(self.targets, dtype=torch.float)

        # set up full pytorch data object
        data = Data(x=node_features, edge_index=edge_indices.t().contiguous(), edge_attr=edge_features, y=targets)

        return data

    # deprecated. Since the node resolve relied on the fact that the first element of each feature string contains the atomic number.
    # def write_mol_file(self, file_path: str):

    #     """Writes the graph in mol format to file.

    #     Args:
    #         filepath (string): The path to the output file.
    #     """

    #     # data to write
    #     data = 'Molecule\n_generated ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n\n'

    #     # set up summary data line
    #     data += str(len(self.nodes)).rjust(3, ' ') + str(len(self.edges)).rjust(3, ' ') + '  0  0  0  0  0  0  0  0999 V2000\n'

    #     # TODO node resolve relies on the fact that the first element of each feature string contains the atomic number
    #     for i in range(len(self.nodes)):
    #         data += '    0.0000    0.0000    0.0000 ' + ElementLookUpTable.get_element_identifier(self.nodes[i][0]).ljust(5, ' ') + '0  0  0  0  0  0  0  0  0  0  0  0\n'

    #     # bond order is read out from first position in edge feature vector
    #     for i in range(len(self.edges)):

    #         bond_order = 1
    #         if self.edges[i][1][0] > 1.5:
    #             bond_order = 2
    #         if self.edges[i][1][0] > 2.5:
    #             bond_order = 3

    #         data += str(self.edges[i][0][0] + 1).rjust(3, ' ') + str(self.edges[i][0][1] + 1).rjust(3, ' ') + str(bond_order).rjust(3, ' ') + '  0  0  0  0 \n'

    #     data += 'M  END'
    #     FileHandler.write_file(file_path, data)

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
        not_visited_nodes = list(range(len(self._nodes)))

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

        if node_index < 0 or node_index > len(self._nodes) - 1:
            raise ValueError('The specified node index is out of range. Valid range: 0 - ' + str(len(self._nodes) - 1) + '. Given: ' + str(node_index) + '.')

        adjacent_nodes = []
        for i in range(len(self._edges)):
            if node_index in self._edges[i].node_indices:
                # get the index of the other node in the edge node list
                other_edge_index = (self._edges[i].node_indices.index(node_index) + 1) % 2
                # get the appropriate node index
                adjacent_node_index = self._edges[i].node_indices[other_edge_index]
                # append to output list
                adjacent_nodes.append(adjacent_node_index)

        return adjacent_nodes

    def get_node_position_dict(self):

        node_position_dict = {}
        for i in range(len(self.positions)):
            node_position_dict[i] = self.positions[i]
        return node_position_dict

    def visualise(self):

        """Plots the graph with appropriate nodes and edges using plotly."""

        # set up node label and feature lists
        node_features = self.nodes_features_list
        node_labels = self.nodes_labels_list

        # set up edge index and feature lists
        edge_indices = self.edges_indices_list + [list(reversed(x)) for x in self.edges_indices_list]
        edge_features = self.edges_features_list * 2

        # get 3d positions
        position_dict = self.get_node_position_dict()

        # seperate the x, y, z coordinates for Plotly
        x_nodes = [position_dict[key][0] for key in position_dict.keys()]
        y_nodes = [position_dict[key][1] for key in position_dict.keys()]
        z_nodes = [position_dict[key][2] for key in position_dict.keys()]

        # we need to create lists that contain the starting and ending coordinates of each edge.
        x_edges, y_edges, z_edges = [], [], []

        # create lists holding midpoints that we will use to anchor text
        xtp, ytp, ztp = [], [], []

        # need to fill these with all of the coordinates
        for edge in edge_indices:

            # format: [beginning, ending, None]
            x_coords = [position_dict[edge[0]][0], position_dict[edge[1]][0], None]
            x_edges += x_coords
            xtp.append(0.5 * (position_dict[edge[0]][0] + position_dict[edge[1]][0]))

            y_coords = [position_dict[edge[0]][1], position_dict[edge[1]][1], None]
            y_edges += y_coords
            ytp.append(0.5 * (position_dict[edge[0]][1] + position_dict[edge[1]][1]))

            z_coords = [position_dict[edge[0]][2], position_dict[edge[1]][2], None]
            z_edges += z_coords
            ztp.append(0.5 * (position_dict[edge[0]][2] + position_dict[edge[1]][2]))

        # get desc text for nodes
        text = [f'{x[0]} | {x[1]}' for x in zip(node_labels, node_features)]
        # create a trace for the nodes
        trace_nodes = go.Scatter3d(
            name='Nodes',
            x=x_nodes,
            y=y_nodes,
            z=z_nodes,
            mode='markers',
            marker=dict(symbol='circle',
                        size=[ElementLookUpTable.get_element_format_size(element) for element in node_labels],
                        color=[ElementLookUpTable.get_element_format_colour(element) for element in node_labels]),
            text=text,
            hoverinfo='text'
        )

        # get desc text for edges
        text = [f'{x[0]} | {x[1]}' for x in zip(edge_indices, edge_features)]
        # create edge text
        trace_weights = go.Scatter3d(x=xtp, y=ytp, z=ztp,
                                     mode='markers',
                                     marker=dict(color='rgb(180,180,180)', size=2),
                                     text=text, hoverinfo='text')

        # create a trace for the edges
        trace_edges = go.Scatter3d(
            name='Edges',
            x=x_edges,
            y=y_edges,
            z=z_edges,
            mode='lines',
            line=dict(color='black', width=3.5),
            hoverinfo='none'
        )

        # Include the traces we want to plot and create a figure
        data = [trace_nodes, trace_edges, trace_weights]
        fig = go.Figure(data=data)

        # get highest and lowest coordinate value to scale graph correctly
        low_coord = min(x_nodes + y_nodes + z_nodes)
        high_coord = max(x_nodes + y_nodes + z_nodes)

        # remove grid and adjust all axes to same range, no legend
        fig.update_layout(title='ID: ' + self.id,
                          title_font_color='teal',
                          paper_bgcolor='#040466',
                          showlegend=False,
                          scene=dict(aspectmode='manual', aspectratio=dict(x=1, y=1, z=1),
                                     xaxis=dict(showbackground=False, visible=False, range=[low_coord, high_coord]),
                                     yaxis=dict(showbackground=False, visible=False, range=[low_coord, high_coord]),
                                     zaxis=dict(showbackground=False, visible=False, range=[low_coord, high_coord])))
        fig.show()
