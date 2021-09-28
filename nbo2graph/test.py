from DataParser import DataParser
from GraphGenerator import GraphGenerator
from FileHandler import FileHandler

from QmAttribute import QmAttribute
from BondDeterminationMode import BondDeterminationMode

from HydrogenMode import HydrogenMode

from ElementLookUpTable import ElementLookUpTable

import matplotlib.pyplot as plt
import networkx as nx
from torch_geometric.utils.convert import to_networkx

import os 
from os.path import isfile, join

# setup target directory path
path = '/home/hkneiding/Desktop/nbo data/'
# setup file list
files = []
for file in os.listdir(path):
    if file.endswith(".log"):
        files.append(file)

# generate vector for attributes to be extracted
attributesToExtract = [QmAttribute.SvpHomoLumoGap]

# set up graph generator with parameters
wibergGG = GraphGenerator(bondDeterminationMode=BondDeterminationMode.Wiberg, bondThreshold=0.3, attributesToExtract=attributesToExtract, hydrogenMode=HydrogenMode.Implicit)
nlmoGG = GraphGenerator(bondDeterminationMode=BondDeterminationMode.NLMO, bondThreshold=0.1, attributesToExtract=attributesToExtract, hydrogenMode=HydrogenMode.Implicit)


graphs = []

for i in range(len(files)):
# for i in range(1):

    print(files[i])
    qmData = DataParser('/home/hkneiding/Desktop/nbo data/' + files[i]).parse()
    #print(qmData.wibergIndexMatrix)
    # generate graph from qmData object
    graphs.append(wibergGG.generateGraph(qmData))
    graphs.append(nlmoGG.generateGraph(qmData))

for graph in graphs:

    # print(graph.attributes)
    #print(graph.nodes)
    # pytorch

    # graph.getAdjacentNodes(49)
    #print(graph.getDisjointSubGraphs())
    print(graph.isConnected())

    print(graph.nodes)
    print(graph.edges)

    pytorchGraphData = graph.getPytorchDataObject()
    G = to_networkx(pytorchGraphData)

    nodeLabelDict = {}
    for i in range(len(graph.nodes)):
        nodeLabelDict[i] = ElementLookUpTable.getElementIdentifier(graph.nodes[i][0])
        # nodeLabelDict[i] = graph.nodes[i][-1]

    # print(nodeLabelDict)

    nx.draw_networkx(G, labels=nodeLabelDict, with_labels=True)
    plt.show()
