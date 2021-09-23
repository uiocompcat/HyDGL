from DataParser import DataParser
from GraphGenerator import GraphGenerator
from FileHandler import FileHandler

from HydrogenMode import HydrogenMode

from ElementLookUpTable import ElementLookUpTable

import matplotlib.pyplot as plt
import networkx as nx
from torch_geometric.utils.convert import to_networkx

gg = GraphGenerator.fromFile('/home/hkneiding/Desktop/full_Gaussian_file_AGOKEN.log',
                             wibergBondThreshold=0.3,
                             hydrogenMode=HydrogenMode.Implicit)
graph = gg.generateGraph()

dp = DataParser('/home/hkneiding/Desktop/full_Gaussian_file_AGOKEN.log')
qm = dp.parse()

# print(qm)

attrs = vars(qm)

print('\n'.join("%s: %s" % item for item in attrs.items()))

exit()

# pytorch

pytorchGraphData = graph.getPytorchDataObject()
G = to_networkx(pytorchGraphData)

nodeLabelDict = {}
for i in range(len(graph.nodes)):
    nodeLabelDict[i] = ElementLookUpTable.getElementIdentifier(graph.nodes[i][0])
    #nodeLabelDict[i] = graph.nodes[i][-1]


nx.draw_networkx(G, labels=nodeLabelDict, with_labels=True)
plt.show()




