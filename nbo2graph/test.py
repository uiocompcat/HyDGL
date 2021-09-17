from DataParser import DataParser
from GraphGenerator import GraphGenerator
from FileHandler import FileHandler

from HydrogenMode import HydrogenMode

from ElementLookUpTable import ElementLookUpTable

import matplotlib.pyplot as plt
import networkx as nx
from torch_geometric.utils.convert import to_networkx

# parse data
dp = DataParser('/home/hkneiding/Desktop/full_Gaussian_file_AGOKEN.log')
qmData = dp.parse()

# build graph
gg = GraphGenerator(qmData, wibergBondThreshold=0.15, hydrogenMode=HydrogenMode.Implicit)
graph = gg.generateGraph()

graph.writeMolFile('/home/hkneiding/Desktop/test.mol')

# pytorch

pytorchGraphData = graph.getPytorchDataObject()
G = to_networkx(pytorchGraphData)

nodeLabelDict = {}
for i in range(len(graph.nodes)):
    # nodeLabelDict[i] = ElementLookUpTable.getElementIdentifier(graph.nodes[i][0])
    nodeLabelDict[i] = graph.nodes[i][-1]


nx.draw_networkx(G, labels=nodeLabelDict, with_labels=True)
plt.show()




