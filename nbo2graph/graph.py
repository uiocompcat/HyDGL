import torch
import warnings
import numpy as np
import networkx as nx
from torch_geometric.data import Data

from nbo2graph.edge import Edge
from nbo2graph.node import Node
from nbo2graph.element_look_up_table import ElementLookUpTable


class Graph:

    """Class for representing chemical graphs with all necessary information."""

    def __init__(self, nodes: list[Node], edges: list[Edge], targets: dict = {}, graph_features: dict = {}, meta_data: dict = {'id': None}):

        """Constructor

        Args:
            metadata (dict): Meta data of the graph.
            nodes (list[list[floats]]): List of node feature vectors.
            edges (list[list[int], list[float]]): List with individual sublists for connected node indices as well as edge features.
            targets (list[float]): List of targets/labels associated to graph (e.g. HOMO-LUMO gap).
            graph_features (list): List of graph level features.
        """

        self._meta_data = meta_data

        self._nodes = nodes
        self._edges = edges
        self._targets = targets
        self._graph_features = graph_features

    @classmethod
    def from_networkx(cls, nx_graph):

        """Alternative way of initialising the Graph object via networkx.

        Returns:
            _type_: The Graph object.
        """

        # graph elements
        id = None
        nodes = []
        edges = []
        targets = {}
        graph_features = {}

        graph_level_keys = nx_graph.graph.keys()

        # obrain id
        if 'id' in graph_level_keys:
            id = nx_graph.graph['id']

        # The following obtains feature and target lists for the graph, nodes and edges.
        # The 'target_' and 'feature_' prefixes are removed before adding them to the
        # respective dicts.

        # iterate through graph level keys
        for key in graph_level_keys:

            # if feature key add to graph features
            if key.startswith('feature_'):
                graph_features[key[len('feature_'):]] = nx_graph.graph[key]

            # if target key add to targets
            if key.startswith('target_'):
                targets[key[len('target_'):]] = nx_graph.graph[key]

        # iterate through nodes
        for node in nx_graph.nodes.data():
            node_features = {}
            node_label = None
            node_position = None
            # iterate through node keys
            for node_feature_key in node[1].keys():
                # if feature key is found add to feature dict
                if node_feature_key.startswith('feature_'):
                    node_features[node_feature_key[len('feature_'):]] = node[1][node_feature_key]
                if node_feature_key == 'node_label':
                    node_label = node[1][node_feature_key]
                if node_feature_key == 'node_position':
                    node_position = node[1][node_feature_key]

            nodes.append(Node(features=node_features, label=node_label, position=node_position))

        # iterate through edges
        for edge in nx_graph.edges.data():
            edge_features = {}
            # iterate through edge keys
            for edge_feature_key in edge[2].keys():
                # if feature key is found add to feature dict
                if edge_feature_key.startswith('feature_'):
                    edge_features[edge_feature_key[len('feature_'):]] = edge[2][edge_feature_key]
            edges.append(Edge([int(edge[0]), int(edge[1])], features=edge_features, is_directed=nx.is_directed(nx_graph)))

        return cls(nodes=nodes, edges=edges, targets=targets, graph_features=graph_features, meta_data={'id': id})

    @property
    def id(self):
        """Getter for id."""

        if 'id' in self._meta_data:
            return self._meta_data['id']
        return None

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
    def nodes_feature_list_list(self):
        """Getter for a list of node feature lists."""
        return [x.feature_list for x in self._nodes]

    @property
    def nodes_feature_dict_list(self):
        """Getter for a list of node feature dicts."""
        return [x.features for x in self._nodes]

    @property
    def nodes_positions_list(self):
        """Getter for a list of node positions."""
        return [x.position for x in self._nodes]

    @property
    def nodes_labels_list(self):
        """Getter for a list of node labels."""
        return [x.label for x in self._nodes]

    @property
    def edges_indices_list(self):
        """Getter for a list of edge indices."""
        return [x.node_indices for x in self._edges]

    @property
    def edges_feature_list_list(self):
        """Getter for a list of edge feature lists."""
        return [x.feature_list for x in self._edges]

    @property
    def edges_feature_dict_list(self):
        """Getter for a list of edge feature dicts."""
        return [x.features for x in self._edges]

    @property
    def graph_type(self):
        """Getter for is_directed."""

        # if there are no edges default to undirected
        if len(self.edges) == 0:
            return 'undirected'

        # count number of directed edges
        directed_edge_count = 0
        for edge in self.edges:
            if edge.is_directed:
                directed_edge_count += 1

        # compare to absolute amount of edges
        if directed_edge_count == len(self.edges):
            return 'directed'
        elif directed_edge_count == 0:
            return 'undirected'
        else:
            return 'mixed'

    def get_networkx_graph_object(self) -> nx.Graph:

        """Generates a networkx graph object.

        Returns:
            networkx.Graph: networkx graph object.
        """

        if self.graph_type == 'directed':
            nx_graph = nx.MultiDiGraph()
        elif self.graph_type == 'undirected':
            nx_graph = nx.MultiGraph()
        else:
            raise NotImplementedError('The graph has directed as well as undirected edges which is not supported by the networkx library.')

        # add CSD code
        nx_graph.graph['id'] = str(self.id)

        # add nodes
        for i, node in enumerate(self.nodes):
            # add features
            nx_graph.add_nodes_from([(i, {f'feature_{k}': v for k, v in node.features.items()})])
            # add miscellaneous data
            if node.label is not None:
                nx_graph.nodes[i]['node_label'] = node.label
            if node.position is not None:
                nx_graph.nodes[i]['node_position'] = node.position

        # add edges
        for edge in self.edges:
            nx_graph.add_edges_from([(edge.node_indices[0], edge.node_indices[1], {f'feature_{k}': v for k, v in edge.features.items()})])

        # add graph features
        for key in self.graph_features.keys():
            nx_graph.graph['feature_' + key] = self.graph_features[key]

        # add targets
        for key in self.targets.keys():
            nx_graph.graph['target_' + key] = self.targets[key]

        return nx_graph

    def get_pytorch_data_object(self, node_class_feature_dict={}, edge_class_feature_dict={}) -> Data:

        """Generates a pytorch data object ready to use for learning/visualisation.

        Returns:
            torch_geometric.data.Data: Pytorch data object containing nodes, edges and edge features.
        """

        # get list of node features
        node_features = []
        for node in self.nodes:
            node_features.append(node.get_one_hot_encoded_feature_list(node_class_feature_dict))

        # get adjacency list and list of corresponding edge features
        edge_indices = []
        edge_features = []
        for edge in self.edges:

            # if directed add only once
            if edge.is_directed:
                edge_indices.append(edge.node_indices)
                edge_features.append(edge.get_one_hot_encoded_feature_list(edge_class_feature_dict))
            # if undirected add twice to account for both directions
            else:
                edge_indices.append(edge.node_indices)
                edge_indices.append(list(reversed(edge.node_indices)))
                edge_features.append(edge.get_one_hot_encoded_feature_list(edge_class_feature_dict))
                edge_features.append(edge.get_one_hot_encoded_feature_list(edge_class_feature_dict))

        # get list of graph features
        graph_features = []
        for key in self.graph_features.keys():
            graph_features.append(self.graph_features[key])

        # get list of targets
        targets = []
        for key in self.targets.keys():
            targets.append(self.targets[key])

        # cast to pytorch tensors
        node_features = torch.tensor(node_features, dtype=torch.float)
        edge_indices = torch.tensor(edge_indices, dtype=torch.long)
        edge_features = torch.tensor(edge_features, dtype=torch.float)
        graph_features = torch.tensor(graph_features, dtype=torch.float)
        targets = torch.tensor(targets, dtype=torch.float)

        # set up full pytorch data object
        data = Data(x=node_features, edge_index=edge_indices.t().contiguous(), edge_attr=edge_features, y=targets, num_nodes=len(self.nodes), graph_attr=graph_features, id=self._meta_data['id'])

        return data

    def is_connected(self) -> bool:

        """Determines whether there are not connected nodes.

        Returns:
            bool: Boolean to describe whether the graph is connected or not.
        """

        # if there is exactly one (disjoint) subgraph then the graph is connected
        if len(self.get_disjoint_sub_graphs()) == 1:
            return True

        # otherwise there are not connected nodes --> disconnected
        return False

    def get_disjoint_sub_graphs_node_indices(self) -> list[list[int]]:

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

    def get_disjoint_sub_graphs(self) -> list[list[int]]:

        """Gets a list of Graph objects of respective disjoint subgraphs.

        Returns:
            list[list[int]]: List of subgraph node indices.
        """

        subgraphs_node_indices = self.get_disjoint_sub_graphs_node_indices()

        subgraphs = []

        for i, subgraph_node_indices in enumerate(subgraphs_node_indices):

            nodes = []
            edge_indices_to_consider = []
            for node_index in subgraph_node_indices:
                # obtain nodes of subgraph
                nodes.append(self.nodes[node_index])

                # get edge list indices of edges in subgraph
                for j, edge in enumerate(self.edges):
                    if node_index in edge.node_indices and j not in edge_indices_to_consider:
                        edge_indices_to_consider.append(j)

            # get edges of subgraph
            edges = []
            for idx in edge_indices_to_consider:
                # update edge indices according to subgraph
                edge_indices = [subgraph_node_indices.index(self.edges[idx].node_indices[0]), subgraph_node_indices.index(self.edges[idx].node_indices[1])]
                edges.append(Edge(edge_indices, features=self.edges[idx].features))

            # set graph
            graph = Graph(nodes, edges, meta_data={'id': str(self.id) + '-subgraph-' + str(i)})
            # append to list
            subgraphs.append(graph)

        return subgraphs

    def get_adjacent_nodes(self, node_index: int) -> list[int]:

        """Gets the indices of adjacent (neighbour by one edge) nodes of a given node based on the edge data.

        Raises:
            ValueError: If the specified node is out of the valid range (either less than zero or higher than the number of nodes).

        Returns:
            list[int]: List of node indices denoting the adjacent nodes.
        """

        # get incoming and outgoing adjecent nodes | remove duplicates
        return list(set(self.get_incoming_adjacent_nodes(node_index) + self.get_outgoing_adjacent_nodes(node_index)))

    def get_incoming_adjacent_nodes(self, node_index: int) -> list[int]:

        """Gets the indices of incoming adjacent (with edges pointing to them) nodes.
        Raises:
            ValueError: If the specified node is out of the valid range (either less than zero or higher than the number of nodes).
        Returns:
            list[int]: List of node indices denoting the incoming adjacent nodes.
        """

        if node_index < 0 or node_index > len(self.nodes) - 1:
            raise ValueError('The specified node index is out of range. Valid range: 0 - ' + str(len(self.nodes) - 1) + '. Given: ' + str(node_index) + '.')

        in_adjacent_node_indices = []
        for edge in self.edges:
            if node_index in edge.node_indices:

                # get the index of the other node in the edge node list
                other_node_edge_list_index = (edge.node_indices.index(node_index) + 1) % 2

                # in case of undirected graph ordering does not matter
                # for directed graphs check that the other node is the source
                if not edge.is_directed or other_node_edge_list_index == 0:
                    in_adjacent_node_index = edge.node_indices[other_node_edge_list_index]
                    in_adjacent_node_indices.append(in_adjacent_node_index)

        return in_adjacent_node_indices

    def get_outgoing_adjacent_nodes(self, node_index: int) -> list[int]:

        """Gets the indices of outgoing adjacent (with edges pointing to them) nodes.
        Raises:
            ValueError: If the specified node is out of the valid range (either less than zero or higher than the number of nodes).
        Returns:
            list[int]: List of node indices denoting the outgoing adjacent nodes.
        """

        if node_index < 0 or node_index > len(self.nodes) - 1:
            raise ValueError('The specified node index is out of range. Valid range: 0 - ' + str(len(self.nodes) - 1) + '. Given: ' + str(node_index) + '.')

        out_adjacent_node_indices = []
        for edge in self.edges:
            if node_index in edge.node_indices:

                # get the index of the other node in the edge node list
                other_node_edge_list_index = (edge.node_indices.index(node_index) + 1) % 2

                # in case of undirected graph ordering does not matter
                # for directed graphs check that the other node is the receiver
                if not edge.is_directed or other_node_edge_list_index == 1:
                    out_adjacent_node_index = edge.node_indices[other_node_edge_list_index]
                    out_adjacent_node_indices.append(out_adjacent_node_index)

        return out_adjacent_node_indices

    def get_adjacency_matrix(self):

        """Gets the adjacency matrix of the graph.

        Returns:
            list[list[float]]: The adjacency matrix.
        """

        adjacency_matrix = []
        for i in range(len(self.nodes)):
            in_adjacent_node_indices = self.get_incoming_adjacent_nodes(i)
            in_adjacency_vector = [1 if node_index in in_adjacent_node_indices else 0 for node_index in range(len(self.nodes))]
            adjacency_matrix.append(in_adjacency_vector)

        return adjacency_matrix

    def get_spectrum(self):

        """Gets the spectrum of the graph.

        Returns:
            list[float]: The spectrum.
        """

        eigen_values = np.linalg.eig(self.get_adjacency_matrix())[0].tolist()
        eigen_values.sort(reverse=True)
        return eigen_values

    def get_node_position_dict(self):

        """Gets a dict of the node positions.

        Returns:
            dict: The dict of positions.
        """

        node_position_dict = {}
        for i in range(len(self.nodes_positions_list)):
            node_position_dict[i] = self.nodes_positions_list[i]
        return node_position_dict

    def get_node_label_dict(self):

        """Gets a dict of the node label.

        Returns:
            dict: The dict of labels.
        """

        node_label_dict = {}
        for i in range(len(self.nodes_labels_list)):
            node_label_dict[i] = self.nodes_labels_list[i]
        return node_label_dict

    def visualise(self):

        """Plots the graph with appropriate nodes and edges using plotly."""

        try:

            import plotly.graph_objects as go

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
            for edge in self.edges_indices_list:

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
            text = [f'{x}' for x in self.nodes_labels_list]
            # text = [f'{x[0]} | {x[1]}' for x in zip(self.nodes_labels_list, self.nodes_feature_dict_list)]
            # create a trace for the nodes
            trace_nodes = go.Scatter3d(
                name='Nodes',
                x=x_nodes,
                y=y_nodes,
                z=z_nodes,
                mode='markers',
                marker=dict(symbol='circle',
                            size=[ElementLookUpTable.get_element_format_size(element) for element in self.nodes_labels_list],
                            color=[ElementLookUpTable.get_element_format_colour(element) for element in self.nodes_labels_list]),
                text=text,
                hoverinfo='text'
            )

            # get desc text for edges
            text = [f'{x}' for x in self.edges_indices_list]
            # text = [f'{x[0]} | {x[1]}' for x in zip(self.edges_indices_list, self.edges_feature_dict_list)]
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
            fig.update_layout(title='ID: ' + str(self.id),
                              title_font_color='teal',
                              paper_bgcolor='#040466',
                              showlegend=False,
                              scene=dict(aspectmode='manual', aspectratio=dict(x=1, y=1, z=1),
                                         xaxis=dict(showbackground=False, visible=False, range=[low_coord, high_coord]),
                                         yaxis=dict(showbackground=False, visible=False, range=[low_coord, high_coord]),
                                         zaxis=dict(showbackground=False, visible=False, range=[low_coord, high_coord])))
            fig.show()

        except ModuleNotFoundError:
            warnings.warn('Cannot plot. The library <plotly> is not installed.')
