import pickle
import matplotlib.pyplot as plt
import numpy as np
import torch
from torch_geometric.loader import DataLoader
import wandb

from tmQMg import tmQMg
from nbo2graph.enums.qm_target import QmTarget
from nbo2graph.graph_generator_settings import GraphGeneratorSettings
from nets import GilmerNet, GilmerNetGraphLevelFeatures
from trainer import Trainer
from tools import calculate_r_squared, get_feature_matrix_dict, get_feature_means_from_feature_matrix_dict, get_feature_stds_from_feature_matrix_dict, set_global_seed, standard_scale_dataset


def main():

    ggs = GraphGeneratorSettings.natQ2(targets=[QmTarget.POLARISABILITY])

    with open('/home/hkneiding/Downloads/outliers_polarizability.pickle', 'rb') as fh:
        outliers = pickle.load(fh)

    dataset = tmQMg(root='/home/hkneiding/Desktop/pyg-dataset-test-dir/run1/', raw_dir='/home/hkneiding/Documents/UiO/Data/tmQMg/extracted/', settings=ggs, exclude=outliers)
    print('Using ' + str(len(dataset)) + ' data points.')
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
    train_graph_feature_matrix = []
    for idx in train_indices:
        # train_node_feature_matrix.extend(dataset.graph_node_features[idx])
        train_node_feature_matrix.extend(dataset[idx]['x'].detach().numpy())
        train_edge_feature_matrix.extend(dataset[idx]['edge_attr'].detach().numpy())
        train_graph_feature_matrix.append(dataset[idx]['graph_attr'].detach().numpy())
    train_node_feature_matrix = np.array(train_node_feature_matrix)
    train_edge_feature_matrix = np.array(train_edge_feature_matrix)
    train_graph_feature_matrix = np.array(train_graph_feature_matrix)

    # get train means and standard deviations for node features
    train_node_feature_means = np.mean(train_node_feature_matrix, axis=0)
    train_node_feature_stds = np.std(train_node_feature_matrix, axis=0)
    # get train means and standard deviations for edge features
    train_edge_feature_means = np.mean(train_edge_feature_matrix, axis=0)
    train_edge_feature_stds = np.std(train_edge_feature_matrix, axis=0)
    # get train means and standard deviations for graph features
    train_graph_feature_means = np.mean(train_graph_feature_matrix, axis=0)
    train_graph_feature_stds = np.std(train_graph_feature_matrix, axis=0)

    if len(np.where(train_node_feature_stds == 0)[0]) > 0:
        print('There are node features with standard deviation 0 within the training set.')

    if len(np.where(train_edge_feature_stds == 0)[0]) > 0:
        print('There are edge features with standard deviation 0 within the training set.')

    if len(np.where(train_graph_feature_stds == 0)[0]) > 0:
        print('There are graph features with standard deviation 0 within the training set.')

    # scale graph, node and edge features according to train means and standard deviations
    for graph in dataset:
        graph['x'] = (graph['x'] - train_node_feature_means) / train_node_feature_stds
        graph['edge_attr'] = (graph['edge_attr'] - train_edge_feature_means) / train_edge_feature_stds
        graph['graph_attr'] = (graph['graph_attr'] - train_graph_feature_means) / train_graph_feature_stds

    # set up data sets
    test_dataset = dataset[test_indices]
    val_dataset = dataset[val_indices]
    train_dataset = dataset[train_indices]

    # set up dataloaders
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

    # TRAINING

    ################################
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    model = GilmerNetGraphLevelFeatures(21, 16, 4)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min',
                                                           factor=0.7, patience=5,
                                                           min_lr=0.00001)
    output = Trainer(model, optimizer, scheduler).run(train_loader, val_loader, test_loader, n_epochs=3000)

    with open('out_ml_pol_graph_features.log', 'w') as fh:
        fh.write(output)
    ################################


def wandb_run():

    with open('/home/hkneiding/Downloads/outliers_polarizability.pickle', 'rb') as fh:
        outliers = pickle.load(fh)

    hyper_param = {
        'data': {
            'dataset': tmQMg,
            'root_dir': '/home/hkneiding/Desktop/pyg-dataset-test-dir/run1/',
            'raw_dir': '/home/hkneiding/Documents/UiO/Data/tmQMg/extracted/',
            'val_set_size': 0.1,
            'test_set_size': 0.1,
            'graph_representation': GraphGeneratorSettings.natQ2,
            'targets': [QmTarget.POLARISABILITY],
            'outliers': outliers
        },
        'model': {
            'name': 'GilmerNet',
            'method': GilmerNet,
            'parameters': {
                'n_node_features': 21,
                'n_edge_features': 16
            }
        },
        'optimizer': {
            'name': 'Adam',
            'method': torch.optim.Adam,
            'parameters': {
                'lr': 0.001
            }
        },
        'scheduler': {
            'name': 'ReduceLrOnPlateau',
            'method': torch.optim.lr_scheduler.ReduceLROnPlateau,
            'parameters': {
                'mode': 'min',
                'factor': 0.7,
                'patience': 5,
                'min_lr': 0.00001
            }
        },
        'scaling': {
            'type': 'standard',
            'features_to_scale': ['x', 'edge_attr', 'graph_attr', 'y']
        },
        'batch_size': 32,
        'n_epochs': 3,
        'seed': 2022
    }

    # wandb.config = hyper_param
    wandb.init(config=hyper_param, project="my-test-project", entity="hkneiding")

    # set seed
    set_global_seed(hyper_param['seed'])

    # setup data set
    dataset = hyper_param['data']['dataset'](root=hyper_param['data']['root_dir'], raw_dir=hyper_param['data']['raw_dir'], settings=hyper_param['data']['graph_representation'](targets=hyper_param['data']['targets']), exclude=hyper_param['data']['outliers'])

    # divide into subsets
    sets = torch.utils.data.random_split(dataset, [len(dataset) - round(hyper_param['data']['val_set_size'] * len(dataset)) - round(hyper_param['data']['test_set_size'] * len(dataset)),
                                                   round(hyper_param['data']['val_set_size'] * len(dataset)),
                                                   round(hyper_param['data']['test_set_size'] * len(dataset))])
    print('Using ' + str(len(dataset)) + ' data points. (train=' + str(len(sets[0])) + ', val=' + str(len(sets[1])) + ', test=' + str(len(sets[2])) + ')')

    # obtain matrices for features and targets for the train set
    train_feature_matrix_dict = get_feature_matrix_dict(sets[0], hyper_param['scaling']['features_to_scale'])
    # scale all sets according to train set feature matrices
    for subset in sets:
        if hyper_param['scaling']['type'] == 'standard':
            subset = standard_scale_dataset(subset, train_feature_matrix_dict)

            # if targets are scaled, retrieve means and stds to reconstruct real errors
            if 'y' in hyper_param['scaling']['features_to_scale']:
                train_target_means = get_feature_means_from_feature_matrix_dict(train_feature_matrix_dict, 'y')
                train_target_stds = get_feature_stds_from_feature_matrix_dict(train_feature_matrix_dict, 'y')
        else:
            raise ValueError('Scaling type not recognized.')

    # set up dataloaders
    train_loader = DataLoader(sets[0], batch_size=hyper_param['batch_size'], shuffle=True)
    val_loader = DataLoader(sets[1], batch_size=hyper_param['batch_size'], shuffle=False)
    test_loader = DataLoader(sets[2], batch_size=hyper_param['batch_size'], shuffle=False)

    # TRAINING

    ################################
    model = hyper_param['model']['method'](**hyper_param['model']['parameters'])
    optimizer = hyper_param['optimizer']['method'](model.parameters(), **hyper_param['optimizer']['parameters'])
    scheduler = hyper_param['scheduler']['method'](optimizer, **hyper_param['scheduler']['parameters'])

    trained_model = Trainer(model, optimizer, scheduler).run(train_loader, val_loader, test_loader, n_epochs=hyper_param['n_epochs'], target_means=train_target_means, target_stds=train_target_stds)
    ################################

    predicted_values = []
    true_values = []
    for batch in test_loader:
        predicted_values.extend(trained_model(batch).cpu().detach().numpy().tolist())
        true_values.extend(batch.y.cpu().detach().numpy().tolist())

    # print(predicted_values)
    # print(true_values)

    # set up canvas
    fig, ax = plt.subplots()
    # base points
    ax.plot(predicted_values, true_values, 'bo')
    # regression line
    z = np.polyfit(predicted_values, true_values, 1)
    p = np.poly1d(z)
    ax.plot(predicted_values, p(predicted_values), "r--")

    # formatting
    ax.text(0.1, 0.9, 'R² = ' + str(calculate_r_squared(np.array(predicted_values), np.array(true_values))), size=15, color='blue', ha='center', va='center', transform=ax.transAxes)
    ax.set_xlabel('Predicted values')
    ax.set_ylabel('True values')

    wandb.log({"r_squared_test": fig})


# - - - entry point - - - #
if __name__ == "__main__":
    wandb_run()
    # main()
