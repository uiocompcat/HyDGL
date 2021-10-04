import os

from nbo2graph.data_parser import DataParser
from nbo2graph.graph_generator import GraphGenerator

from nbo2graph.qm_atrribute import QmAttribute
from nbo2graph.bond_determination_mode import BondDeterminationMode

from nbo2graph.node_feature import NodeFeature
from nbo2graph.edge_feature import EdgeFeature

from nbo2graph.hydrogen_mode import HydrogenMode

from nbo2graph.element_look_up_table import ElementLookUpTable

import matplotlib.pyplot as plt
import networkx as nx
from torch_geometric.utils.convert import to_networkx

# setup target directory path
path = '/home/hkneiding/Desktop/nbo data/'
# setup file list
files = []
for file in os.listdir(path):
    if file.endswith(".log"):
        files.append(file)

node_features = [NodeFeature.ATOMIC_NUMBERS]
edge_features = [EdgeFeature.BOND_ORDER]

# generate vector for attributes to be extracted
attributes_to_extract = [QmAttribute.SVP_ELECTRONIC_ENERGY]

# set up graph generator with parameters
wiberg_g_g = GraphGenerator(node_features=node_features, edge_feautres=edge_features,
                            bond_determination_mode=BondDeterminationMode.NLMO, bond_threshold=0.3, attributes_to_extract=attributes_to_extract, hydrogen_mode=HydrogenMode.IMPLICIT)
#nlmo_g_g = GraphGenerator(bond_determination_mode=BondDeterminationMode.NLMO, bond_threshold=0.1, attributes_to_extract=attributes_to_extract, hydrogen_mode=HydrogenMode.IMPLICIT)


graphs = []

# for i in range(len(files)):
for i in range(1):

    print(files[i])
    qm_data = DataParser('/home/hkneiding/Desktop/nbo data/' + files[i]).parse()
    #print(qm_data.wiberg_index_matrix)
    # generate graph from qm_data object
    graphs.append(wiberg_g_g.generate_graph(qm_data))
    # graphs.append(nlmo_g_g.generate_graph(qm_data))

for graph in graphs:

    # print(graph.attributes)
    #print(graph.nodes)
    # pytorch

    # graph.get_adjacent_nodes(49)
    #print(graph.get_disjoint_sub_graphs())
    # print(graph.is_connected())

    # print(graph.nodes)
    # print(graph.edges)
    print(graph.attributes)

    pytorch_graph_data = graph.get_pytorch_data_object()
    G = to_networkx(pytorch_graph_data)

    node_label_dict = {}
    for i in range(len(graph.nodes)):
        node_label_dict[i] = ElementLookUpTable.get_element_identifier(graph.nodes[i][0])
        # node_label_dict[i] = graph.nodes[i][-1]

    # print(node_label_dict)

    # nx.draw_networkx(G, labels=node_label_dict, with_labels=True)
    # plt.show()
