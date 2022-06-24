from inspect import getargs
import os
import pickle
import pandas as pd
import numpy as np
from sklearn.cluster import k_means
from tqdm import tqdm
import dask.dataframe as dd
from nbo2graph.edge import Edge
from nbo2graph.enums.bond_order_type import BondOrderType
from nbo2graph.enums.edge_feature import EdgeFeature
from nbo2graph.enums.edge_type import EdgeType
from nbo2graph.enums.graph_feature import GraphFeature
from nbo2graph.enums.hydrogen_mode import HydrogenMode
from nbo2graph.enums.node_feature import NodeFeature
from nbo2graph.enums.qm_target import QmTarget
from nbo2graph.enums.sopa_edge_feature import SopaEdgeFeature
from nbo2graph.enums.sopa_resolution_mode import SopaResolutionMode
from nbo2graph.file_handler import FileHandler
from nbo2graph.graph import Graph
from nbo2graph.node import Node
from nbo2graph.graph_generator_settings import GraphGeneratorSettings
from nbo2graph.qm_data import QmData
# from nbo2graph.datasets.tmQMg import tmQMg
from time import sleep
from nbo2graph.tools import Tools


from scripts.data_parser import DataParser
from scripts.tmQMg import tmQMg
from nbo2graph.graph_generator import GraphGenerator

import networkx as nx


def main():

    # # setup target directory path
    path = '/home/hkneiding/Documents/UiO/Data/tmQMg/raw/'
    files = [file for file in os.listdir(path) if file.split('.')[-1] == 'log']

    ggs = GraphGeneratorSettings.natQ3([])
    gg = GraphGenerator(settings=ggs)
    for file in tqdm(files):
        qm_data = DataParser(path + file).parse()
        qm_data_object = QmData.from_dict(qm_data)

        graph = gg.generate_graph(qm_data_object)

        print(graph.edges[0].features)

        exit()

        if not graph.is_connected():
            graph.visualise()

    exit()

    # qm_data = DataParser('/home/hkneiding/Documents/UiO/Data/tmQMg/raw/' + 'FEYBOC.log').parse()
    # qm_data_object = QmData.from_dict(qm_data)
    # ggs = GraphGeneratorSettings.natQ3([QmTarget.SVP_HOMO_LUMO_GAP])
    # gg = GraphGenerator(settings=ggs)
    # graph = gg.generate_graph(qm_data_object)
    # graph.visualise()

    exit()

    nx.write_gml(graph.get_networkx_graph_object(), '/home/hkneiding/Desktop/' + file_name + '.gml')

    # nx_graph = graph.get_networkx_graph_object()
    # print(nx_graph.nodes.data())
    exit()

    nx.write_gml(graph.get_networkx_graph_object(), '/home/hkneiding/Desktop/test.gml')

    pyg = graph.get_pytorch_data_object(edge_class_feature_dict={'nbo_type': ['BD', '3C', 'None']})
    print(pyg['edge_attr'][0])
    # graph.visualise()

    exit()
    # nx_h2o_graph = nx.MultiGraph()
    # nx_h2o_graph.add_nodes_from([
    #     (0, {"x": 8}),
    #     (1, {"x": 1}),
    #     (2, {"x": 1})
    # ])
    # nx_h2o_graph.add_edges_from([
    #     (0, 1),
    #     (0, 2)
    # ])
    # nm = nx.algorithms.isomorphism.categorical_node_match('x', 0)

    nx.write_gml(graph.get_networkx_graph_object(), '/home/hkneiding/Desktop/test.gml')
    # exit()

    # print(nx_h2o_graph.is_directed())

    # print(subgraphs)
    # for subgraph in subgraphs:

    #     nx_subgraph = subgraph.get_networkx_graph_object()
    #     # print(nx_subgraph.is_directed())

    #     print(nx.is_isomorphic(nx_subgraph, nx_h2o_graph, node_match=nm))

    # print(graph.networkx_graph.edge_attr_dict_factory)
    # print(graph.get_networkx_graph_object().nodes(data=True))
    # nx.write_gml(graph.get_networkx_graph_object(), '/home/hkneiding/Desktop/' + file_name + '.gml')

    exit()

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

    ggs = GraphGeneratorSettings.default(edge_types=[EdgeType.NBO_BONDING_ORBITALS], hydrogen_mode=HydrogenMode.EXPLICIT,
                                         edge_features=[EdgeFeature.BOND_ORBITAL_MAX, EdgeFeature.BOND_ORBITAL_S_SYMMETRY], bond_threshold=0.2)
    gg = GraphGenerator(settings=ggs)
    graph = gg.generate_graph(DataParser('/home/hkneiding/Documents/UiO/Data/tmQM/the_random_500/ZUYHEG.log').parse_to_qm_data_object())
    # graph = gg.generate_graph(DataParser('/home/hkneiding/Documents/UiO/Data/tmQM/06_data_lake/OREDIA.log').parse_to_qm_data_object())
    # graph = gg.generate_graph(DataParser('/home/hkneiding/Documents/UiO/Data/tmQM/06_data_lake/LEZYOG.log').parse_to_qm_data_object())

    # print(graph)
    # graph = Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
    #               [Edge([0, 1], features=[0], is_directed=True), Edge([0, 2], features=[0], is_directed=False), Edge([0, 3], features=[0], is_directed=True), Edge([3, 2], features=[0], is_directed=True), Edge([2, 4], features=[0], is_directed=False)])
    # print(graph.get_spectrum())
    graph.visualise()

    # for graph in graphs:

    #     print(graph)
    #     graph.visualise()


def get_number_connected_graphs():

    # directory that holds the extracted raw data
    ext_data_dir = '/home/hkneiding/Documents/UiO/Data/tmQMg/extracted/'
    files = [x for x in os.listdir(ext_data_dir) if x.split('.')[-1] == 'json']

    # get settings
    settings = GraphGeneratorSettings.default(edge_types=[EdgeType.BOND_ORDER_METAL, EdgeType.NBO_BONDING_ORBITALS], bond_order_mode=BondOrderType.WIBERG)

    # set up thesholds
    bond_thresholds = np.linspace(0.2, 0.2, 1)
    # set up output array
    n_connected_graphs_list = []

    for bond_threshold in tqdm(bond_thresholds):

        # set same threshold for all atom types
        settings.bond_threshold_metal = bond_threshold
        # set up graph generator with parameters
        gg = GraphGenerator(settings)

        # generate graphs with appropriate settings
        graphs = []

        for file in tqdm(files):

            # get QmData object
            qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(ext_data_dir + file))
            graphs.append(gg.generate_graph(qm_data))

        n_connected_graphs = 0
        # determine the number of connected graphs
        for j in range(len(graphs)):
            if graphs[j].is_connected():
                n_connected_graphs += 1

        n_connected_graphs_list.append(n_connected_graphs)

    print(n_connected_graphs_list)

def extract_gaussian_data():

    raw_file_path = '/home/hkneiding/Documents/UiO/Data/tmQMg/raw/'
    extracted_file_path = '/home/hkneiding/Documents/UiO/Data/tmQMg/extracted/'

    raw_files = [file for file in os.listdir(raw_file_path)]

    for raw_file in raw_files:

        try:
            qm_data_dict = DataParser(raw_file_path + raw_file).parse()
            FileHandler.write_dict_to_json_file(extracted_file_path + raw_file.replace('.log', '') + '.json', qm_data_dict)
        except ValueError:
            print(raw_file)

def get_disconnected_graphs(ggs: GraphGeneratorSettings):

    # directory that holds the extracted raw data
    ext_data_dir = '/home/hkneiding/Documents/UiO/Data/tmQMg/extracted/'

    # list of all files
    files = [x for x in os.listdir(ext_data_dir)]
    # specify graph generator
    gg = GraphGenerator(ggs)

    # iterate through files, build graphs and check for connectivity
    for file in tqdm(files):

        # skip files that are not in JSON format
        if file.split('.')[-1] != 'json':
            continue

        # get QmData object
        qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(ext_data_dir + file))
        # build graph
        graph = gg.generate_graph(qm_data)

        # check connectivity
        if not graph.is_connected():
            tqdm.write(file)


def show_molecule():

    # symmetry failure of NBO examples: KOCTED, ZUJFEP, WAHNOK

    #WEJFUN

    qm_data = DataParser('/home/hkneiding/Documents/UiO/Data/tmQMg/raw/' + 'ORUHIT.log').parse()
    qm_data_object = QmData.from_dict(qm_data)
    ggs = GraphGeneratorSettings.natQ2([QmTarget.SVP_HOMO_LUMO_GAP])
    gg = GraphGenerator(settings=ggs)
    graph = gg.generate_graph(qm_data_object)
    print(graph.is_connected())
    graph.visualise()



# - - - entry point - - - #
if __name__ == "__main__":



    # # list of all files
    # files = [x for x in os.listdir(ext_data_dir)]
    
    # qm_data_list = []
    # # iterate through files, build graphs and check for connectivity
    # for file in tqdm(files):

    #     # skip files that are not in JSON format
    #     if file.split('.')[-1] != 'json':
    #         continue

    #     # get QmData object
    #     qm_data = QmData.from_dict(FileHandler.read_dict_from_json_file(ext_data_dir + file))
    #     qm_data_list.append(qm_data)

    get_number_connected_graphs()
    # show_molecule()
    # main()
    
    # extract_gaussian_data()
    #extract_gaussian_data_to_pandas()
    #read_extracted_data()

    # ggs = GraphGeneratorSettings.default(edge_types=[EdgeType.BOND_ORDER_METAL, EdgeType.BOND_ORDER_NON_METAL], bond_threshold=0.1, bond_threshold_metal=0.05)
    # get_disconnected_graphs(ggs)
