import os
import time

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
    files = files[11:12]
    print(files)

    # get settings
    settings = GraphGeneratorSettings.from_file('./run.config')

    # set up graph generator with parameters
    gg = GraphGenerator(settings)

    graphs = [gg.generate_graph(DataParser(path + file).parse()) for file in files]

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

    #     print(end1 - start1)
    #     print(end2 - start2)

    end = time.time()
    print('Elapsed time: ' + str(end - start))

    for graph in graphs:

        print(graph)
        graph.visualise()


# def visualise_graph(graph):

#     # set up node label and feature lists
#     node_features = graph.nodes
#     node_labels = graph.labels

#     # set up edge index and feature lists
#     edge_indices = [x[0] for x in graph.edges] + [list(reversed(x[0])) for x in graph.edges]
#     edge_features = [x[1] for x in graph.edges * 2]

#     # get 3d positions
#     position_dict = graph.get_node_position_dict()

#     # seperate the x, y, z coordinates for Plotly
#     x_nodes = [position_dict[key][0] for key in position_dict.keys()]
#     y_nodes = [position_dict[key][1] for key in position_dict.keys()]
#     z_nodes = [position_dict[key][2] for key in position_dict.keys()]

#     # we need to create lists that contain the starting and ending coordinates of each edge.
#     x_edges, y_edges, z_edges = [], [], []

#     # create lists holding midpoints that we will use to anchor text
#     xtp, ytp, ztp = [], [], []

#     # need to fill these with all of the coordinates
#     for edge in edge_indices:

#         # format: [beginning, ending, None]
#         x_coords = [position_dict[edge[0]][0], position_dict[edge[1]][0], None]
#         x_edges += x_coords
#         xtp.append(0.5 * (position_dict[edge[0]][0] + position_dict[edge[1]][0]))

#         y_coords = [position_dict[edge[0]][1], position_dict[edge[1]][1], None]
#         y_edges += y_coords
#         ytp.append(0.5 * (position_dict[edge[0]][1] + position_dict[edge[1]][1]))

#         z_coords = [position_dict[edge[0]][2], position_dict[edge[1]][2], None]
#         z_edges += z_coords
#         ztp.append(0.5 * (position_dict[edge[0]][2] + position_dict[edge[1]][2]))

#     # get desc text for nodes
#     text = [f'{x[0]} | {x[1]}' for x in zip(node_labels, node_features)]
#     # create a trace for the nodes
#     trace_nodes = go.Scatter3d(
#         name='Nodes',
#         x=x_nodes,
#         y=y_nodes,
#         z=z_nodes,
#         mode='markers',
#         marker=dict(symbol='circle',
#                     size=[atom_format_dict[element]['size'] for element in node_labels],
#                     color=[atom_format_dict[element]['color'] for element in node_labels]),
#         text=text,
#         hoverinfo='text'
#     )

#     # get desc text for edges
#     text = [f'{x[0]} | {x[1]}' for x in zip(edge_indices, edge_features)]
#     # create edge text
#     trace_weights = go.Scatter3d(x=xtp, y=ytp, z=ztp,
#                                  mode='markers',
#                                  marker=dict(color='rgb(180,180,180)', size=2),
#                                  text=text, hoverinfo='text')

#     # create a trace for the edges
#     trace_edges = go.Scatter3d(
#         name='Edges',
#         x=x_edges,
#         y=y_edges,
#         z=z_edges,
#         mode='lines',
#         line=dict(color='black', width=3.5),
#         hoverinfo='none'
#     )

#     # Include the traces we want to plot and create a figure
#     data = [trace_nodes, trace_edges, trace_weights]
#     fig = go.Figure(data=data)

#     # get highest and lowest coordinate value to scale graph correctly
#     low_coord = min(x_nodes + y_nodes + z_nodes)
#     high_coord = max(x_nodes + y_nodes + z_nodes)

#     # remove grid and adjust all axes to same range, no legend
#     fig.update_layout(showlegend=False,
#                       scene=dict(xaxis=dict(showbackground=False, visible=False, range=[low_coord, high_coord]),
#                                  yaxis=dict(showbackground=False, visible=False, range=[low_coord, high_coord]),
#                                  zaxis=dict(showbackground=False, visible=False, range=[low_coord, high_coord])))
#     fig.show()


# entry point
if __name__ == "__main__":
    main()
