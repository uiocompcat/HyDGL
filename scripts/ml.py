import numpy as np
import torch
import torch.nn.functional as F
from torch.nn import GRU, Linear, ReLU, Sequential
from torch_geometric.loader import DataLoader
from torch_geometric.nn import NNConv, Set2Set

from tmQMg import tmQMg
from nbo2graph.enums.qm_target import QmTarget
from nbo2graph.graph_generator_settings import GraphGeneratorSettings


# specify your own network here
class GilmerNet(torch.nn.Module):

    def __init__(self, n_node_features, n_edge_features, dim=64, set2set_steps=3, n_atom_jumps=3):
        super().__init__()

        self.n_atom_jumps = n_atom_jumps

        self.lin0 = torch.nn.Linear(n_node_features, dim)

        nn = Sequential(Linear(n_edge_features, 128), ReLU(), Linear(128, dim * dim))
        self.conv = NNConv(dim, dim, nn, aggr='mean')
        self.gru = GRU(dim, dim)

        self.set2set = Set2Set(dim, processing_steps=set2set_steps)
        self.lin1 = torch.nn.Linear(2 * dim, dim)
        self.lin2 = torch.nn.Linear(dim, 1)

    def forward(self, data):
        out = F.relu(self.lin0(data.x))
        h = out.unsqueeze(0)

        for i in range(self.n_atom_jumps):
            m = F.relu(self.conv(out, data.edge_index, data.edge_attr))
            out, h = self.gru(m.unsqueeze(0), h)
            out = out.squeeze(0)

        out = self.set2set(out, data.batch)
        out = F.relu(self.lin1(out))
        out = self.lin2(out)
        return out.view(-1)


class Trainer():

    def __init__(self, model, optimizer, scheduler=None):

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        self.model = model.to(self.device)
        self.optimizer = optimizer
        self.scheduler = scheduler

    def train(self, train_loader):
        self.model.train()
        loss_all = 0

        for data in train_loader:
            data = data.to(self.device)
            self.optimizer.zero_grad()
            loss = F.mse_loss(self.model(data), data.y)
            loss.backward()
            loss_all += loss.item() * data.num_graphs
            self.optimizer.step()
        return loss_all / len(train_loader.dataset)

    def test(self, loader):
        self.model.eval()
        error = 0

        for data in loader:
            data = data.to(self.device)
            error += (self.model(data) - data.y).abs().sum().item()  # MAE
        return error / len(loader.dataset)

    def run(self, train_loader, val_loader, test_loader):
        best_val_error = None
        for epoch in range(1, 301):

            # get learning rate from scheduler
            if self.scheduler is not None:
                lr = self.scheduler.optimizer.param_groups[0]['lr']

            loss = self.train(train_loader)
            val_error = self.test(val_loader)

            # learning rate scheduler step
            if self.scheduler is not None:
                self.scheduler.step(val_error)

            if best_val_error is None or val_error <= best_val_error:
                test_error = self.test(test_loader)
                best_val_error = val_error

            print(f'Epoch: {epoch:03d}, LR: {lr:7f}, Loss: {loss:.7f}, '
                  f'Val MAE: {val_error:.7f}, Test MAE: {test_error:.7f}')


def main():

    ggs = GraphGeneratorSettings.natQ2(targets=[QmTarget.POLARISABILITY])

    dataset = tmQMg(root='/home/hkneiding/Desktop/pyg-dataset-test-dir/run1/', raw_dir='/home/hkneiding/Documents/UiO/Data/tmQMg/extracted/', settings=ggs)

    np.random.seed(2022)

    # get a random permutation of indices
    shuffled_indices = np.random.permutation(len(dataset))

    # assign indices to train, val and test sets
    test_indices = shuffled_indices[:round(0.1 * len(dataset))]
    val_indices = shuffled_indices[round(0.1 * len(dataset)):round(0.2 * len(dataset))]
    train_indices = shuffled_indices[round(0.2 * len(dataset)):]

    # build node and edge feature matrices for the training data points
    train_node_feature_matrix = []
    train_edge_feature_matrix = []
    for idx in train_indices:
        train_node_feature_matrix.extend(dataset.graph_node_features[idx])
        train_edge_feature_matrix.extend(dataset.graph_edge_features[idx])
    train_node_feature_matrix = np.array(train_node_feature_matrix)
    train_edge_feature_matrix = np.array(train_edge_feature_matrix)

    # get train means and standard deviations for node features
    train_node_feature_means = np.mean(train_node_feature_matrix, axis=0)
    train_node_feature_stds = np.std(train_node_feature_matrix, axis=0)
    # get train means and standard deviations for edge features
    train_edge_feature_means = np.mean(train_edge_feature_matrix, axis=0)
    train_edge_feature_stds = np.std(train_edge_feature_matrix, axis=0)

    if len(np.where(train_node_feature_stds == 0)[0]) > 0:
        print('There are node features with standard deviation 0 within the training set.')

    if len(np.where(train_edge_feature_stds == 0)[0]) > 0:
        print('There are edge features with standard deviation 0 within the training set.')

    # scale node and edge features according to train means and standard deviations
    for graph in dataset:
        graph['x'] = (graph['x'] - train_node_feature_means) / train_node_feature_stds
        graph['edge_attr'] = (graph['edge_attr'] - train_edge_feature_means) / train_edge_feature_stds

    # set up data sets
    test_dataset = dataset[test_indices]
    val_dataset = dataset[val_indices]
    train_dataset = dataset[train_indices]

    # set up dataloaders
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

    # TRAINING

    model = GilmerNet(21, 16)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min',
                                                           factor=0.7, patience=5,
                                                           min_lr=0.00001)

    Trainer(model, optimizer, scheduler).run(train_loader, val_loader, test_loader)


# - - - entry point - - - #
if __name__ == "__main__":
    main()
