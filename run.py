import os

from nbo2graph.element_look_up_table import ElementLookUpTable

from nbo2graph.graph_generator_settings import GraphGeneratorSettings

from nbo2graph.data_parser import DataParser
from nbo2graph.graph_generator import GraphGenerator

import networkx as nx
import matplotlib.pyplot as plt
from torch_geometric.utils.convert import to_networkx


def main():

    # setup target directory path
    path = '/home/hkneiding/Desktop/nbo data/'
    # setup file list
    files = [file for file in os.listdir(path) if file.endswith(".log")]
    print(files)

    settings = GraphGeneratorSettings.from_file('./run.config')

    # set up graph generator with parameters
    gg = GraphGenerator(settings)

    graphs = []
    # for i in range(len(files)):
    for i in range(1, 2, 1):

        print(files[i])
        qm_data = DataParser('/home/hkneiding/Desktop/nbo data/' + files[i]).parse()
        # generate graph from qm_data object
        graphs.append(gg.generate_graph(qm_data))

    print()
    for graph in graphs:

        # print(graph.attributes)
        print('Nodes')
        print(graph.nodes)
        print()
        print('Edges')
        print(graph.edges)
        print()
        print('Graph features')
        print(graph.graph_features)
        print()
        # pytorch

        # graph.get_adjacent_nodes(49)
        # print(graph.get_disjoint_sub_graphs())
        # print(graph.is_connected())

        # print(graph.nodes)
        # print(graph.edges)
        # print(graph.attributes)

        pytorch_graph_data = graph.get_pytorch_data_object()
        G = to_networkx(pytorch_graph_data)

        # node_label_dict = {}
        # for i in range(len(graph.nodes)):
        #     node_label_dict[i] = ElementLookUpTable.get_element_identifier(graph.nodes[i][0])
        #     # node_label_dict[i] = graph.nodes[i][-1]

        # nx.draw_networkx(G, labels=node_label_dict, with_labels=True)
        nx.draw_networkx(G, with_labels=True)
        plt.show()


# entry point
if __name__ == "__main__":
    main()
