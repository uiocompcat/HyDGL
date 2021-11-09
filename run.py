import os
import sys
from statistics import mean
import time

from pympler import asizeof

# import plotly.graph_objects as go

from nbo2graph.graph_generator_settings import GraphGeneratorSettings

from nbo2graph.data_parser import DataParser
from nbo2graph.graph_generator import GraphGenerator

# import networkx as nx
# import matplotlib.pyplot as plt
# from torch_geometric.utils.convert import to_networkx


def main():

    start = time.time()

    # setup target directory path
    # path = '/home/hkneiding/Desktop/nbo data/'
    path = '/home/hkneiding/Desktop/nbo data/the_random_500/'
    # setup file list
    files = [file for file in os.listdir(path) if file.endswith(".log")]
    files = files[0:1]
    # print(files)

    # get settings
    settings = GraphGeneratorSettings.from_file('./run.config')

    # set up graph generator with parameters
    gg = GraphGenerator(settings)

    graphs = [gg.generate_graph(DataParser(path + file).parse()) for file in files]

    # time_a = []
    # time_b = []

    # graphs = []
    # for i in range(len(files)):
    #     print(files[i] + ' -- ' + str(i + 1))
    #     start1 = time.time()
    #     qm_data = DataParser(path + files[i]).parse()
    #     end1 = time.time()

    #     # generate graph from qm_data object
    #     start2 = time.time()
    #     graphs.append(gg.generate_graph(qm_data))
    #     end2 = time.time()

    #     time_a.append(end1 - start1)
    #     time_b.append(end2 - start2)

    end = time.time()
    print('Elapsed time: ' + str(end - start))

    print(graphs[0])

    # print(mean(time_a))
    # print(mean(time_b))
    # print(asizeof.asizeof(graphs))

    # for graph in graphs:

    #     print(graph)
    #     graph.visualise()


# entry point
if __name__ == "__main__":
    main()
