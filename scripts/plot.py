import numpy as np
import matplotlib.pyplot as plt

from tools import calculate_r_squared


def plot_metal_center_group_histogram(dataset, meta_data_dict: dict):

    group_counts = np.zeros(10)
    for graph in dataset:
        group_counts[meta_data_dict[graph.id]['metal_center_group'] - 3] += 1

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(np.arange(3, 13), group_counts)
    ax.set_xlabel('Metal center group')
    ax.set_ylabel('Counter')

    return fig


def plot_correlation(predicted_values: list, true_values: list):

    # set up canvas
    fig, ax = plt.subplots(figsize=(10, 6))
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

    return fig


def plot_error_by_metal_center_group(predicted_values: list, true_values: list, metal_center_groups: list):

    group_counts = np.zeros(10)
    group_accumulated_errors = np.zeros(10)
    for i in range(len(predicted_values)):
        group_accumulated_errors[metal_center_groups[i] - 3] += np.abs(predicted_values[i] - true_values[i])
        group_counts[metal_center_groups[i] - 3] += 1

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(np.arange(3, 13), group_accumulated_errors / group_counts)
    ax.set_xlabel('Metal center group')
    ax.set_ylabel('Mean average deviation')

    return fig
