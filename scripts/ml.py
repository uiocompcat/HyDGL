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
class Net(torch.nn.Module):
    def __init__(self):
        super().__init__()

        dim = 64
        self.lin0 = torch.nn.Linear(21, dim)

        nn = Sequential(Linear(16, 128), ReLU(), Linear(128, dim * dim))
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

def main():

    ggs = GraphGeneratorSettings.natQ2(targets=[QmTarget.POLARISABILITY])

    dataset = tmQMg(root='/home/hkneiding/Desktop/pyg-dataset-test-dir/run1/', raw_dir='/home/hkneiding/Documents/UiO/Data/tmQMg/extracted/', settings=ggs)

    np.random.seed(2022)

    # get a random permutation of indices
    shuffled_indices = np.random.permutation(len(dataset))

    # assign indices to train, val and test sets
    test_indices = shuffled_indices[:5000]
    val_indices = shuffled_indices[5000:10000]
    train_indices = shuffled_indices[10000:]

    # build node and edge feature matrices for the training data points
    train_node_feature_matrix = []
    train_edge_feature_matrix = []
    for idx in train_indices:
        train_node_feature_matrix.extend(dataset.graph_node_features[idx])
        train_edge_feature_matrix.extend(dataset.graph_edge_features[idx])
    train_node_feature_matrix = np.array(train_node_feature_matrix)
    train_edge_feature_matrix = np.array(train_edge_feature_matrix)

    # get train means and standard deviations for node features
    train_node_feature_means = np.mean(train_node_feature_matrix[train_indices], axis=0)
    train_node_feature_stds = np.std(train_node_feature_matrix[train_indices], axis=0)
    # get train means and standard deviations for edge features
    train_edge_feature_means = np.mean(train_edge_feature_matrix[train_indices], axis=0)
    train_edge_feature_stds = np.std(train_edge_feature_matrix[train_indices], axis=0)

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
            error += (model(data) - data.y ).abs().sum().item()  # MAE
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
    main()
