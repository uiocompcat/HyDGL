import torch
from datetime import datetime
from torch_geometric.data import Data

from FileHandler import FileHandler
from ElementLookUpTable import ElementLookUpTable

class Graph:

    """Class for reading relevant data from QM output files."""

    def __init__(self, nodes, edges, attributes=[]):

        """Constructor

        Args:
            nodes (list[list[floats]]): List of node features.
            edges (list[list[int], list[float]]): List with individual sublists for connected node indices as well as edge features.
            attributes (list): List of attributes/labels associated to graph (e.g. HOMO-LUMO gap).
        """

        self.nodes = nodes
        self.edges = edges
        self.attributes = attributes

    def getPytorchDataObject(self) -> Data:

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

    def writeMolFile(self, filePath: str):

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

    def isConnected(self) -> bool:

        """Determines whether there are not connected nodes.

        Returns:
            bool: Boolean to describe whether the graph is connected or not.
        """

        # if there is exactly one (disjoint) subgraph then the graph is connected
        if len(self.getDisjointSubGraphs()) == 1:
            return True

        # otherwise there are not connected --> disconnected
        return False

    def getDisjointSubGraphs(self) -> list[list[int]]:

        """Gets a list of lists of node indices belonging to respective disjoint subgraphs.

        Returns:
            list[list[int]]: List of subgraph node indices.
        """

        # output list
        disjointSubGraphs = []
        # contains all node indices
        notVisitedNodes = list(range(len(self.nodes)))
        
        while len(notVisitedNodes) > 0:

            # list to store the nodes part of the current (disjoint) sub graph
            currentSubGraphIndices = []
            # set up new queue with first element of not yet visited nodes
            nodeQueue = [notVisitedNodes[0]]

            while len(nodeQueue) > 0:

                # get neighbours of current node
                neighbours = self.getAdjacentNodes(nodeQueue[0])
                # dequeue
                currentSubGraphIndices.append(nodeQueue[0])
                nodeQueue.pop(0)
                # enqueue (only enque nodes that have not been visited before)
                nodeQueue.extend(list(set(neighbours) - set(currentSubGraphIndices)))

            # update list of not visited nodes
            notVisitedNodes = list(set(notVisitedNodes) - set(currentSubGraphIndices))
            # append subgraph to output list
            disjointSubGraphs.append(currentSubGraphIndices)

        # return disjoint sub graphs as sub lists
        return disjointSubGraphs

    def getAdjacentNodes(self, nodeIndex: int) -> list[int]:

        """Gets the indices of adjacent (neighbour by one edge) nodes of a given node based on the edge data.

        Raises:
            ValueError: If the specified node is out of the valid range (either less than zero or higher than the number of nodes).

        Returns:
            list[int]: List of node indices denoting the adjacent nodes.
        """

        if nodeIndex < 0 or nodeIndex > len(self.nodes):
            raise ValueError('The specified node index is out of range. Valid range: 0 - ' + str(len(self.nodes) - 1) + '. Given: ' + str(nodeIndex) + '.')

        adjacentNodes = []
        for i in range(len(self.edges)):
            if nodeIndex in self.edges[i][0]:
                # get the index of the other node in the edge node list
                otherEdgeIndex = (self.edges[i][0].index(nodeIndex) + 1) % 2
                # get the appropriate node index
                adjacentNodeIndex = self.edges[i][0][otherEdgeIndex]
                # append to output list
                adjacentNodes.append(adjacentNodeIndex)

        return adjacentNodes