import os

import pickle
import numpy as np
from nbo2graph.enums.bond_determination_mode import BondDeterminationMode
from nbo2graph.enums.edge_feature import EdgeFeature
from nbo2graph.enums.hydrogen_mode import HydrogenMode
from nbo2graph.enums.node_feature import NodeFeature
from nbo2graph.graph import Graph

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

    # load from file
    file_to_read = open("/home/hkneiding/Desktop/nbo data/the_random_500/r500-qmdata.pickle", "rb")
    qm_data_list = pickle.load(file_to_read)
    file_to_read.close()

    ggs = GraphGeneratorSettings(bond_determination_mode=BondDeterminationMode.WIBERG)
    gg = GraphGenerator(settings=ggs)
    for i in range(len(qm_data_list)):

        graph = gg.generate_graph(qm_data_list[i])
        if not graph.is_connected():
            graph.visualise()
            break


    # ggs = GraphGeneratorSettings(bond_determination_mode=BondDeterminationMode.WIBERG,
    #                              edge_features=[EdgeFeature.BOND_ORBITAL_MAX, EdgeFeature.BOND_ORBITAL_DATA_S])
    # gg = GraphGenerator(settings=ggs)
    # graph = gg.generate_graph(DataParser('/home/hkneiding/Desktop/nbo data/OREDIA.log').parse())
    # graph = gg.generate_graph(DataParser('/home/hkneiding/Desktop/nbo data/the_random_500/LEZYOG.log').parse())

    # print(graph)
    # graph.visualise()

    # for graph in graphs:

    #     print(graph)
    #     graph.visualise()


def get_not_connected_graphs(qm_data_list):

    # # get settings
    # settings = GraphGeneratorSettings.from_file('./run.config')
    settings = GraphGeneratorSettings.default()
    settings.bond_determination_mode = BondDeterminationMode.NLMO
    # # set up graph generator with parameters
    gg = GraphGenerator(settings)

    bond_thresholds = np.linspace(0, 0.1, 100)
    n_connected_graphs = np.zeros(len(bond_thresholds))
    for i in range(len(bond_thresholds)):

        gg.settings.bond_threshold = bond_thresholds[i]
        graphs = [gg.generate_graph(qm_data) for qm_data in qm_data_list]

        for j in range(len(graphs)):

            if graphs[j].is_connected():
                n_connected_graphs[i] += 1

    print(n_connected_graphs)


# entry point
if __name__ == "__main__":
    main()
