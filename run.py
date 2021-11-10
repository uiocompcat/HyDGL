import os

import pickle
import numpy as np
from nbo2graph.enums.bond_determination_mode import BondDeterminationMode
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

    # # load from file
    # file_to_read = open("/home/hkneiding/Desktop/nbo data/the_random_500/r500-qmdata.pickle", "rb")
    # qm_data_list = pickle.load(file_to_read)
    # file_to_read.close()

    # # get settings
    # settings = GraphGeneratorSettings.from_file('./run.config')

    # # set up graph generator with parameters
    # gg = GraphGenerator(settings)

    # graphs = [gg.generate_graph(qm_data) for qm_data in qm_data_list]

    ggs = GraphGeneratorSettings.default()
    gg = GraphGenerator(settings=ggs)
    graph = gg.generate_graph(DataParser('/home/hkneiding/Desktop/nbo data/OREDIA.log').parse())

    print(graph)
    graph.visualise()

    # for graph in graphs:

    #     print(graph)
    #     graph.visualise()


# entry point
if __name__ == "__main__":
    main()
