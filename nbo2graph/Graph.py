import torch
from datetime import datetime
from torch_geometric.data import Data

from FileHandler import FileHandler
from ElementLookUpTable import ElementLookUpTable

class Graph:

    """Class for reading relevant data from QM output files."""

    def __init__(self, nodes, edges, attributes=None):

        """Constructor

        Args:
            nodes (list[list[floats]]): List of node features.
            edges (list[list[int], list[float]]): List with individual sublists for connected node indices as well as edge features.
        """

        self.attributes = attributes
        self.nodes = nodes
        self.edges = edges

    def getPytorchDataObject(self):

        """Generates a pytorch data object ready to use for learning/visualisation.

        Returns:
            torch_geometric.data.Data: Pytorch data object containing nodes, edges and edge features.
        """

        # set up pytorch object for edges
        # include reverse edges (to account for both directions)
        edgeIndices = torch.tensor([x[0] for x in self.edges] + [list(reversed(x[0])) for x in self.edges], dtype=torch.long)
        # set up pytorch object for edge features
        # duplicated list to account for the attributes of the additional reverse edges
        edgeFeatures = torch.tensor([x[1] for x in self.edges * 2], dtype=torch.float)

        # set up pytorch object for nodes
        nodeFeatures = torch.tensor(self.nodes, dtype=torch.float)

        # set up full pytorch data object
        data = Data(x=nodeFeatures, edge_index=edgeIndices.t().contiguous(), edge_attr=edgeFeatures)

        return data

    def writeMolFile(self, filePath):

        """Writes the graph in mol format to file.

        Args:
            filepath (string): The path to the output file.
        """

        # data to write
        data = 'Molecule\nGenerated ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n\n'

        # set up summary data line
        data += str(len(self.nodes)).rjust(3, ' ') + str(len(self.edges)).rjust(3, ' ') + '  0  0  0  0  0  0  0  0999 V2000\n'

        # TODO node resolve relies on the fact the the first element of each feature string contains the atomic number
        for i in range(len(self.nodes)):
            data += '    0.0000    0.0000    0.0000 ' + ElementLookUpTable.getElementIdentifier(self.nodes[i][0]).ljust(5, ' ') + '0  0  0  0  0  0  0  0  0  0  0  0\n'

        # bond order is read out from first position in edge feature vector
        for i in range(len(self.edges)):

            bondOrder = 1
            if self.edges[i][1][0] > 1.5:
                bondOrder = 2
            if self.edges[i][1][0] > 2.5:                
                bondOrder = 3

            data += str(self.edges[i][0][0] + 1).rjust(3, ' ') + str(self.edges[i][0][1] + 1).rjust(3, ' ') + str(bondOrder).rjust(3, ' ') + '  0  0  0  0 \n'

        data += 'M  END'
        FileHandler.writeFile(filePath, data)