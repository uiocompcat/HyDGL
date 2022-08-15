import random
import torch
import numpy as np


def set_global_seed(seed: int) -> None:

    """Sets the random seed for python, numpy and pytorch."""

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def get_feature_matrix_dict(dataset, feature_keys: list[str]):

    """Gets a dictionary of feature matrices based on a given list of feature keys.

    Args:
        dataset (Data): The pytorch dataset.
        feature_keys (list[str]): The list of feature keys to get feature matrices for.

    Returns:
        dict: The dict of feature matrices.
    """

    feature_matrix_dict = {}

    for data in dataset:
        for feature_key in feature_keys:

            if feature_key not in feature_matrix_dict.keys():
                feature_matrix_dict[feature_key] = []

            feature_matrix_dict[feature_key].extend(data[feature_key].detach().numpy())

    for feature_key in feature_matrix_dict.keys():
        feature_matrix_dict[feature_key] = np.array(feature_matrix_dict[feature_key])

    return feature_matrix_dict


def standard_scale_dataset(dataset, feature_matrix_dict: dict):

    """Standard scales a dataset based on a given dictionary of feature_matrices. Each feature that is present in the feature matrix dict
    will be scaled in the dataset.

    Args:
        dataset (Data): The pytorch dataset.
        feature_matrix_dict (dict): The feature matrix dict where each key should correspond to a feature in the data.

    Returns:
        Data: The scaled pytorch dataset.
    """

    feature_means = {}
    feature_stds = {}

    for feature_key in feature_matrix_dict.keys():
        feature_means[feature_key] = np.mean(feature_matrix_dict[feature_key], axis=0)
        feature_stds[feature_key] = np.std(feature_matrix_dict[feature_key], axis=0)

    for data in dataset:
        for feature_key in feature_matrix_dict.keys():
            data[feature_key] = (data[feature_key] - feature_means[feature_key]) / feature_stds[feature_key]

    return dataset


def get_feature_means_from_feature_matrix_dict(feature_matrix_dict: dict, feature_key: str):
    return np.mean(feature_matrix_dict[feature_key], axis=0, keepdims=True)


def get_feature_stds_from_feature_matrix_dict(feature_matrix_dict: dict, feature_key: str):
    return np.std(feature_matrix_dict[feature_key], axis=0, keepdims=True)


def calculate_r_squared(predictions, targets):

    """Calculates the R^2 value for given y and y_hat.

    Returns:
        float: The R^2 value.
    """

    target_mean = np.mean(targets)
    return 1 - (np.sum(np.power(targets - predictions, 2)) / np.sum(np.power(targets - target_mean, 2)))
