import os
import pickle
import numpy as np
from sklearn.cluster import k_means
from nbo2graph.edge import Edge
from nbo2graph.enums.bond_order_type import BondOrderType
from nbo2graph.enums.edge_feature import EdgeFeature
from nbo2graph.enums.edge_type import EdgeType
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

from scripts.data_parser import DataParser
from scripts.tmQMg import tmQMg
from nbo2graph.graph_generator import GraphGenerator

import networkx as nx


def main():

    # setup target directory path
    path = '/home/hkneiding/Documents/UiO/Data/tmQMg/raw/'
    file_name = 'ZUYHEG'
    qm_data = DataParser(path + file_name + '.log').parse()

    # FileHandler.write_dict_to_json_file('/home/hkneiding/Desktop/' + file_name + '.json', qm_data)

    qm_data_object = QmData.from_dict(qm_data)

    ggs = GraphGeneratorSettings.default(edge_types=[EdgeType.NBO_BONDING_ORBITALS], hydrogen_mode=HydrogenMode.EXPLICIT,
                                         edge_features=[
                                             EdgeFeature.NBO_TYPE,
                                             EdgeFeature.BOND_ORBITAL_MAX,
                                             EdgeFeature.ANTIBOND_ORBITAL_MIN,
                                             EdgeFeature.BOND_ENERGY_MIN_MAX_DIFFERENCE,
                                             EdgeFeature.ANTIBOND_ENERGY_MIN_MAX_DIFFERENCE,
                                             EdgeFeature.BOND_ORBITAL_DATA_S,
                                             EdgeFeature.BOND_ORBITAL_DATA_P,
                                             EdgeFeature.BOND_ORBITAL_DATA_D,
                                             EdgeFeature.ANTIBOND_ORBITAL_DATA_S,
                                             EdgeFeature.ANTIBOND_ORBITAL_DATA_P,
                                             EdgeFeature.ANTIBOND_ORBITAL_DATA_D
                                            ],
                                         node_features=[
                                             NodeFeature.ATOMIC_NUMBER,
                                             NodeFeature.NATURAL_ATOMIC_CHARGE,
                                             NodeFeature.NATURAL_ELECTRON_POPULATION_VALENCE,
                                             NodeFeature.NATURAL_ELECTRON_CONFIGURATION_S,
                                             NodeFeature.NATURAL_ELECTRON_CONFIGURATION_P,
                                             NodeFeature.NATURAL_ELECTRON_CONFIGURATION_D,
                                             NodeFeature.LONE_PAIR_MAX,
                                             NodeFeature.LONE_VACANCY_MIN,
                                             NodeFeature.LONE_PAIR_ENERGY_MIN_MAX_DIFFERENCE,
                                             NodeFeature.LONE_VACANCY_ENERGY_MIN_MAX_DIFFERENCE,
                                             NodeFeature.LONE_PAIR_S,
                                             NodeFeature.LONE_PAIR_P,
                                             NodeFeature.LONE_PAIR_D,
                                             NodeFeature.LONE_VACANCY_S,
                                             NodeFeature.LONE_VACANCY_P,
                                             NodeFeature.LONE_VACANCY_D],
                                         targets=[QmTarget.SVP_HOMO_LUMO_GAP],
                                         bond_threshold_metal=0.05)

    ggs = GraphGeneratorSettings.natQ2([QmTarget.SVP_HOMO_LUMO_GAP])

    gg = GraphGenerator(settings=ggs)
    graph = gg.generate_graph(qm_data_object)
    subgraphs = graph.get_disjoint_sub_graphs()

    nx.write_gml(graph.get_networkx_graph_object(), '/home/hkneiding/Desktop/test.gml')

    graph.get_pytorch_data_object({0: ['BD', '3C', 'None']})

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
                                         edge_features=[EdgeFeature.BOND_ORBITAL_MAX, EdgeFeature.BOND_ORBITAL_DATA_S], bond_threshold=0.2)
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


def test_ml():

    ggs = GraphGeneratorSettings.default(edge_types=[EdgeType.SOPA],
                                         sopa_interaction_threshold=1,
                                         sopa_edge_features=[SopaEdgeFeature.ACCEPTOR_NBO_TYPE, SopaEdgeFeature.DONOR_NBO_TYPE],
                                         edge_features=[EdgeFeature.NBO_TYPE, EdgeFeature.WIBERG_BOND_ORDER],
                                         targets=[QmTarget.POLARISABILITY])

    ggs = GraphGeneratorSettings.default(edge_types=[EdgeType.NBO_BONDING_ORBITALS])

    dataset = tmQMg('/home/hkneiding/Desktop/pyg-dataset-test-dir/', ggs)
    # dataset.clear_graph_directories()

    exit()

    # dataset.clear_graph_directories()
    # dataset.process()

    # print(dataset[0].is_undirected())

    import torch
    import torch.nn.functional as F
    from torch.nn import GRU, Linear, ReLU, Sequential

    from torch_geometric.loader import DataLoader
    from torch_geometric.nn import NNConv, Set2Set

    test_dataset = dataset[:100]
    val_dataset = dataset[100:200]
    train_dataset = dataset[200:]
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

    dim = 64

    # # Normalize targets to mean = 0 and std = 1.
    # mean = dataset.data.y.mean(dim=0, keepdim=True)
    # std = dataset.data.y.std(dim=0, keepdim=True)
    # dataset.data.y = (dataset.data.y - mean) / std
    # mean, std = mean[:].item(), std[:].item()
    std = 1

    class Net(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.lin0 = torch.nn.Linear(dataset.num_features, dim)

            nn = Sequential(Linear(12, 128), ReLU(), Linear(128, dim * dim))
            self.conv = NNConv(dim, dim, nn, aggr='mean')
            self.gru = GRU(dim, dim)

            self.set2set = Set2Set(dim, processing_steps=3)
            self.lin1 = torch.nn.Linear(2 * dim, dim)
            self.lin2 = torch.nn.Linear(dim, 1)

        def forward(self, data):
            out = F.relu(self.lin0(data.x))
            h = out.unsqueeze(0)

            for i in range(3):
                m = F.relu(self.conv(out, data.edge_index, data.edge_attr))
                out, h = self.gru(m.unsqueeze(0), h)
                out = out.squeeze(0)

            out = self.set2set(out, data.batch)
            out = F.relu(self.lin1(out))
            out = self.lin2(out)
            return out.view(-1)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = Net().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min',
                                                           factor=0.7, patience=5,
                                                           min_lr=0.00001)

    def train(epoch):
        model.train()
        loss_all = 0

        for data in train_loader:
            data = data.to(device)
            optimizer.zero_grad()
            loss = F.mse_loss(model(data), data.y)
            loss.backward()
            loss_all += loss.item() * data.num_graphs
            optimizer.step()
        return loss_all / len(train_loader.dataset)

    def test(loader):
        model.eval()
        error = 0

        for data in loader:
            data = data.to(device)
            error += (model(data) * std - data.y * std).abs().sum().item()  # MAE
        return error / len(loader.dataset)

    best_val_error = None
    for epoch in range(1, 301):
        lr = scheduler.optimizer.param_groups[0]['lr']
        loss = train(epoch)
        val_error = test(val_loader)
        scheduler.step(val_error)

        if best_val_error is None or val_error <= best_val_error:
            test_error = test(test_loader)
            best_val_error = val_error

        print(f'Epoch: {epoch:03d}, LR: {lr:7f}, Loss: {loss:.7f}, '
              f'Val MAE: {val_error:.7f}, Test MAE: {test_error:.7f}')


# - - - entry point - - - #
if __name__ == "__main__":
    # extract_tmqm()
    main()
    # check_3c()
    # test_ml()
    # extract_gaussian_data()
