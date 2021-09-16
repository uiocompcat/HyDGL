from DataParser import DataParser
from GraphGenerator import GraphGenerator
from FileHandler import FileHandler

import matplotlib.pyplot as plt
import networkx as nx
import torch
from torch_geometric.data import Data
from torch_geometric.utils.convert import to_networkx

# parse data
dp = DataParser('/home/hkneiding/Desktop/full_Gaussian_file_AGOKEN.log')
qmData = dp.parse()

# build graph
gg = GraphGenerator(qmData)
graph = gg.generateGraph()

# print(graph)
# FileHandler.writeMolFile('/home/hkneiding/Desktop/test.mol', graph)

print(graph['nodes'])

edge_index = torch.tensor([[0, 1, 1, 2],
                           [1, 0, 2, 1]], dtype=torch.long)
x = torch.tensor([[-1], [0], [1]], dtype=torch.float)

data = Data(x=x, edge_index=edge_index)
G = to_networkx(data)

nx.draw_networkx(G)
plt.show()