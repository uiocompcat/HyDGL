import os
import tarfile
import pickle
from typing import Generator
import numpy as np
from nbo2graph.edge import Edge
from nbo2graph.enums.bond_order_type import BondOrderType
from nbo2graph.enums.edge_feature import EdgeFeature
from nbo2graph.enums.edge_type import EdgeType
from nbo2graph.enums.hydrogen_mode import HydrogenMode
from nbo2graph.enums.node_feature import NodeFeature
from nbo2graph.enums.sopa_resolution_mode import SopaResolutionMode
from nbo2graph.graph import Graph
from nbo2graph.node import Node
from nbo2graph.graph_generator_settings import GraphGeneratorSettings

from nbo2graph.data_parser import DataParser
from nbo2graph.graph_generator import GraphGenerator

# import networkx as nx
# import matplotlib.pyplot as plt
# from torch_geometric.utils.convert import to_networkx


def main():

    # # setup target directory path
    # path = '/home/hkneiding/Desktop/nbo data/the_random_500/'
    # files = [file for file in os.listdir(path) if file.endswith(".log")]
    # qm_data_list = [DataParser(path + file).parse() for file in files]

    # # write to file
    # with open('/home/hkneiding/Desktop/r500-qmdata.pickle', 'wb') as handle:
    #     pickle.dump(qm_data_list, handle)

    # # load from file
    # file_to_read = open("/home/hkneiding/Desktop/nbo data/the_random_500/r500-qmdata.pickle", "rb")
    # qm_data_list = pickle.load(file_to_read)
    # file_to_read.close()

    # ggs = GraphGeneratorSettings(bond_determination_mode=BondDeterminationMode.WIBERG, bond_threshold=0.3, bond_threshold_metal=0.05)
    # gg = GraphGenerator(settings=ggs)

    # for i in range(len(qm_data_list)):
    #     graph = gg.generate_graph(qm_data_list[i])
    #     if not graph.is_connected():
    #         # graph.visualise()
    #         # break
    #         print(i)

    ggs = GraphGeneratorSettings.default(edge_types=[EdgeType.BOND_ORDER_NON_METAL, EdgeType.BOND_ORDER_METAL], hydrogen_mode=HydrogenMode.EXPLICIT,
                                         edge_features=[EdgeFeature.WIBERG_BOND_ORDER], bond_threshold=0.2)
    gg = GraphGenerator(settings=ggs)
    graph = gg.generate_graph(DataParser('/home/hkneiding/Documents/UiO/Data/tmQM/the_random_500/ZUYHEG.log').parse_to_qm_data_object())
    # graph = gg.generate_graph(DataParser('/home/hkneiding/Documents/UiO/Data/tmQM/06_data_lake/OREDIA.log').parse_to_qm_data_object())
    # graph = gg.generate_graph(DataParser('/home/hkneiding/Documents/UiO/Data/tmQM/06_data_lake/LEZYOG.log').parse_to_qm_data_object())

    # print(graph)
    # graph = Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
    #               [Edge([0, 1], features=[0], is_directed=True), Edge([0, 2], features=[0], is_directed=False), Edge([0, 3], features=[0], is_directed=True), Edge([3, 2], features=[0], is_directed=True), Edge([2, 4], features=[0], is_directed=False)])
    # print(graph.get_spectrum())
    # graph.visualise()

    # for graph in graphs:

    #     print(graph)
    #     graph.visualise()


def get_number_connected_graphs(qm_data_list):

    # get settings
    settings = GraphGeneratorSettings.default(edge_types=[EdgeType.BOND_ORDER_METAL, EdgeType.BOND_ORDER_NON_METAL], bond_order_mode=BondOrderType.WIBERG)

    # set up thesholds
    bond_thresholds = np.linspace(0, 0.1, 10)
    # set up output array
    n_connected_graphs = np.zeros(len(bond_thresholds))

    for i in range(len(bond_thresholds)):

        # set same threshold for all atom types
        settings.bond_threshold_metal = bond_thresholds[i]
        settings.bond_threshold = bond_thresholds[i]
        # set up graph generator with parameters
        gg = GraphGenerator(settings)

        # generate graphs with appropriate settings
        graphs = [gg.generate_graph(qm_data) for qm_data in qm_data_list]

        # determine the number of connected graphs
        for j in range(len(graphs)):
            if graphs[j].is_connected():
                n_connected_graphs[i] += 1

    print(n_connected_graphs)


# - - - entry point - - - #
if __name__ == "__main__":
    # extract_tmqm()
    main()
