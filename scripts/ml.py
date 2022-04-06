import pickle
import torch
from torch_geometric.loader import DataLoader
import wandb

from tmQMg import tmQMg
from nbo2graph.enums.qm_target import QmTarget
from nbo2graph.graph_generator_settings import GraphGeneratorSettings
from nets import GilmerNet, GilmerNetGraphLevelFeatures
from trainer import Trainer
from tools import get_feature_matrix_dict, get_feature_means_from_feature_matrix_dict, get_feature_stds_from_feature_matrix_dict, set_global_seed, standard_scale_dataset
from plot import plot_metal_center_group_histogram, plot_correlation, plot_error_by_metal_center_group, wandb_plot_error_by_metal_center_group


def run_ml(hyper_param: dict, wandb_project_name: str = 'tmQMg-natQgraph2', wandb_entity: str = 'hkneiding'):

    # wandb.config = hyper_param
    wandb.init(config=hyper_param, project=wandb_project_name, entity=wandb_entity)

    # set seed
    set_global_seed(hyper_param['seed'])

    # setup data set
    dataset = hyper_param['data']['dataset'](root=hyper_param['data']['root_dir'], raw_dir=hyper_param['data']['raw_dir'], settings=hyper_param['data']['graph_representation'](targets=hyper_param['data']['targets']), exclude=hyper_param['data']['outliers'])

    # divide into subsets
    sets = torch.utils.data.random_split(dataset, [len(dataset) - round(hyper_param['data']['val_set_size'] * len(dataset)) - round(hyper_param['data']['test_set_size'] * len(dataset)),
                                                   round(hyper_param['data']['val_set_size'] * len(dataset)),
                                                   round(hyper_param['data']['test_set_size'] * len(dataset))])
    print('Using ' + str(len(dataset)) + ' data points. (train=' + str(len(sets[0])) + ', val=' + str(len(sets[1])) + ', test=' + str(len(sets[2])) + ')')

    # obtain matrices for features and targets of the train set
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

    # obtain dictionary of meta data information
    meta_data_dict = dataset.get_meta_data_dict()

    # set up model
    model = hyper_param['model']['method'](**hyper_param['model']['parameters'])
    # set up optimizer and scheduler
    optimizer = hyper_param['optimizer']['method'](model.parameters(), **hyper_param['optimizer']['parameters'])
    scheduler = hyper_param['scheduler']['method'](optimizer, **hyper_param['scheduler']['parameters'])

    # run
    trainer = Trainer(model, optimizer, scheduler)
    trained_model = trainer.run(train_loader, val_loader, test_loader, n_epochs=hyper_param['n_epochs'], target_means=train_target_means, target_stds=train_target_stds)

    # get test set predictions and ground truths
    train_predicted_values = []
    train_true_values = []
    train_metal_center_groups = []
    for batch in train_loader:
        train_predicted_values.extend(trainer.predict_batch(batch, target_means=train_target_means, target_stds=train_target_stds))
        train_true_values.extend((batch.y.cpu().detach().numpy() * train_target_stds + train_target_means).tolist())
        train_metal_center_groups.extend([meta_data_dict[id]['metal_center_group'] for id in batch.id])

    # get test set predictions and ground truths
    val_predicted_values = []
    val_true_values = []
    val_metal_center_groups = []
    for batch in val_loader:
        val_predicted_values.extend(trainer.predict_batch(batch, target_means=train_target_means, target_stds=train_target_stds))
        val_true_values.extend((batch.y.cpu().detach().numpy() * train_target_stds + train_target_means).tolist())
        val_metal_center_groups.extend([meta_data_dict[id]['metal_center_group'] for id in batch.id])

    # get test set predictions and ground truths
    test_predicted_values = []
    test_true_values = []
    test_metal_center_groups = []
    for batch in test_loader:
        test_predicted_values.extend(trainer.predict_batch(batch, target_means=train_target_means, target_stds=train_target_stds))
        test_true_values.extend((batch.y.cpu().detach().numpy() * train_target_stds + train_target_means).tolist())
        test_metal_center_groups.extend([meta_data_dict[id]['metal_center_group'] for id in batch.id])

    # log plots

    tmp_file_path = '/tmp/image.png'

    plot_metal_center_group_histogram(sets[0], sets[1], sets[2], meta_data_dict, file_path=tmp_file_path)
    wandb.log({'Metal center group distribution among sets': wandb.Image(tmp_file_path)})

    plot_correlation(train_predicted_values, train_true_values, file_path=tmp_file_path)
    wandb.log({'Training set prediction correlation': wandb.Image(tmp_file_path)})

    plot_correlation(val_predicted_values, val_true_values, file_path=tmp_file_path)
    wandb.log({'Validation set prediction correlation': wandb.Image(tmp_file_path)})

    plot_correlation(test_predicted_values, test_true_values, file_path=tmp_file_path)
    wandb.log({'Test set prediction correlation': wandb.Image(tmp_file_path)})

    plot_error_by_metal_center_group(test_predicted_values, test_true_values, test_metal_center_groups, file_path=tmp_file_path)
    wandb.log({'Test set error by metal center group': wandb.Image(tmp_file_path)})

    wandb.log({"test_set_error_by_metal": wandb_plot_error_by_metal_center_group(test_predicted_values, test_true_values, test_metal_center_groups)})

    # end run
    wandb.finish(exit_code=0)


def run_graph_feat_big():

    with open('/home/hkneiding/Downloads/outliers_polarizability.pickle', 'rb') as fh:
        outliers = pickle.load(fh)

    hyper_param = {
        'name': 'graph feat big+',
        'data': {
            'dataset': tmQMg,
            'root_dir': '/home/hkneiding/Desktop/pyg-dataset-test-dir/run13/',
            'raw_dir': '/home/hkneiding/Documents/UiO/Data/tmQMg/extracted/',
            'val_set_size': 0.1,
            'test_set_size': 0.1,
            'graph_representation': GraphGeneratorSettings.natQ2extended,
            'targets': [QmTarget.POLARISABILITY],
            'outliers': outliers
        },
        'model': {
            'name': 'GilmerNet',
            'method': GilmerNetGraphLevelFeatures,
            'parameters': {
                'n_node_features': 21,
                'n_edge_features': 18,
                'n_graph_features': 4,
                'dim': 128,
                'set2set_steps': 6,
                'n_atom_jumps': 6
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
        'n_epochs': 300,
        'seed': 2022
    }

    run_ml(hyper_param)


def run_extended():

    with open('/home/hkneiding/Downloads/outliers_polarizability.pickle', 'rb') as fh:
        outliers = pickle.load(fh)

    hyper_param = {
        'name': 'extended',
        'data': {
            'dataset': tmQMg,
            'root_dir': '/home/hkneiding/Desktop/pyg-dataset-test-dir/run3/',
            'raw_dir': '/home/hkneiding/Documents/UiO/Data/tmQMg/extracted/',
            'val_set_size': 0.1,
            'test_set_size': 0.1,
            'graph_representation': GraphGeneratorSettings.natQ2extended,
            'targets': [QmTarget.POLARISABILITY],
            'outliers': outliers
        },
        'model': {
            'name': 'GilmerNet',
            'method': GilmerNet,
            'parameters': {
                'n_node_features': 21,
                'n_edge_features': 18
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
        'n_epochs': 300,
        'seed': 2022
    }

    run_ml(hyper_param)


# - - - entry point - - - #
if __name__ == "__main__":

    # api = wandb.Api()
    # run = api.run("hkneiding/tmQMg-natQgraph2/17j02lpm")

    run_graph_feat_big()
    # run_reduced()
    # run_extended()
