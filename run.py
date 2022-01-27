import os
import pickle
import numpy as np
from torchaudio import datasets
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
from nbo2graph.graph_generator import GraphGenerator

# import networkx as nx
# import matplotlib.pyplot as plt
from torch_geometric.utils.convert import to_networkx


def main():

    # setup target directory path
    path = '/home/hkneiding/Documents/UiO/Data/tmQM/raw/'
    file_name = 'ZUYHEG.log'
    qm_data = DataParser(path + file_name).parse()

    FileHandler.write_dict_to_json_file('/home/hkneiding/Desktop/ZUYHEG.json', qm_data)

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


def check_3c():

    # setup target directory path
    path = '/home/hkneiding/Documents/UiO/Data/tmQM/the_random_500/'
    files = [file for file in os.listdir(path) if file.endswith(".log")]
    qm_data_list = [DataParser(path + file).parse_to_qm_data_object() for file in files]

    for i in range(len(qm_data_list)):

        for j in range(len(qm_data_list[i].bond_3c_data)):

            for k in range(len(qm_data_list[i].bond_pair_data)):

                if qm_data_list[i].bond_pair_data[k].atom_indices[0] in qm_data_list[i].bond_3c_data[j].atom_indices and \
                   qm_data_list[i].bond_pair_data[k].atom_indices[1] in qm_data_list[i].bond_3c_data[j].atom_indices:

                    print(qm_data_list[i].id)


def test_ml():

    dataset = tmQMg('/home/hkneiding/Documents/UiO/Data/tmQM/', GraphGeneratorSettings.default(edge_types=[EdgeType.SOPA],
                                                                                               sopa_interaction_threshold=1,
                                                                                               sopa_edge_features=[SopaEdgeFeature.ACCEPTOR_NBO_TYPE, SopaEdgeFeature.DONOR_NBO_TYPE],
                                                                                               edge_features=[EdgeFeature.NBO_TYPE, EdgeFeature.WIBERG_BOND_ORDER],
                                                                                               targets=[QmTarget.POLARISABILITY]))

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
