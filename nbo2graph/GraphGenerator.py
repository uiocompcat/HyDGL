from Graph import Graph
from QmData import QmData
from HydrogenMode import HydrogenMode

class GraphGenerator:

    """Class to generate appropriate graphs based on supplied QM data."""

    def __init__(self, qmData: QmData, wibergBondThreshold=0.3, wibergHydrogenCountThreshold=None, hydrogenMode=HydrogenMode.Explicit):
        """Constructor

        Args:
            qmData (QmData): QmData object that holds all of the extracted QM data.
            wibergBondThreshold (float): Threshold value defining the lower bound for considering bonds.
            wibergHydrogenCountThreshold(float): Threshold value defining the lower bound for considering hydrogens as bound for implicit mode.
            hydrogenMode (HydrogenMode): Operation mode defining the way to handle hydrogens.
        """

        self.qmData = qmData

        self.wibergBondThreshold = wibergBondThreshold
        self.hydrogenMode = hydrogenMode
        self.wibergHydrogenCountThreshold = wibergHydrogenCountThreshold

        # set threshold to general bond threshold if not specified
        if wibergHydrogenCountThreshold == None:
            self.wibergHydrogenCountThreshold = self.wibergBondThreshold

    def generateGraph(self):

        # get nodes and edges
        nodes = self.getNodes()
        edges = self.getEdges()

        # check validity of nodes
        self.validateNodeList(nodes)
        # check validity of edges
        self.validateEdgeList(edges, len(nodes))

        return Graph(nodes, edges)

    def getEdges(self):

        # pre read data for efficiency
        bondPairAtomIndices = [x[0] for x in self.qmData.bondPairData]

        edges = []
        # iterate over half triangle matrix to determine bonds
        for i in range(len(self.qmData.wibergIndexMatrix) - 1):
            for j in range(i + 1, len(self.qmData.wibergIndexMatrix), 1):
                
                # if larger than threshold --> add bond
                if self.qmData.wibergIndexMatrix[i][j] > self.wibergBondThreshold:
                   
                    # append the atom indices (pos 0)
                    # and Wiberg bond index as a feature (pos 1)

                    # add all hydrogens in explicit mode
                    if self.hydrogenMode == HydrogenMode.Explicit:
                        edges.append([[i, j], [self.qmData.wibergIndexMatrix[i][j]]])
                    # ignore hydrogens in omit and implicit mode
                    elif self.hydrogenMode == HydrogenMode.Omit or self.hydrogenMode == HydrogenMode.Implicit:
                        if self.qmData.atomicNumbers[i] == 1 or self.qmData.atomicNumbers[j] == 1:
                            continue
                        else:
                            edges.append([[i, j], [self.qmData.wibergIndexMatrix[i][j]]])

        # rescale node referenes in edges if explicit hydrogens were omitted
        if self.hydrogenMode == HydrogenMode.Omit or self.hydrogenMode == HydrogenMode.Implicit:
            # get list of indices in use
            bondAtomIndices = list(set([item for sublist in [x[0] for x in edges] for item in sublist]))
            bondAtomIndices.sort()
            # loop through edges an replace node references
            for i in range(len(edges)):
                edges[i][0][0] = bondAtomIndices.index(edges[i][0][0])
                edges[i][0][1] = bondAtomIndices.index(edges[i][0][1])

        # add additional (NBO) features to edges
        for i in range(len(edges)):
            
            # check if NBO data for the respective bond is available
            # if so add to feature vector
            # otherwise add zeros to feature vector
            if edges[i][0] in bondPairAtomIndices:
                bondPairIndex = bondPairAtomIndices.index(edges[i][0])
                edges[i][1].extend(self.qmData.bondPairData[bondPairIndex][1])
            else:
                edges[i][1].extend([0,0,0,0])

        return edges

    def getNodes(self):

        # pre read data for efficiency
        lonePairAtomIndices = [x[0] for x in self.qmData.lonePairData]
        loneVacancyAtomIndices = [x[0] for x in self.qmData.loneVacancyData]

        # get hydrogen counts for heavy atoms in implicit mode
        hydrogenCounts = []
        if self.hydrogenMode == HydrogenMode.Implicit:
            for i in range(self.qmData.nAtoms):
                # skip hydrogens
                if self.qmData.atomicNumbers[i] == 1:
                    hydrogenCounts.append(0)
                else:
                    # determine hydrogen count
                    hydrogenCounts.append(self.determineHydrogenCount(i))

        nodes = []
        for i in range(self.qmData.nAtoms):

            # skip if hydrogen mode is not explicit
            if self.hydrogenMode == HydrogenMode.Omit or self.hydrogenMode == HydrogenMode.Implicit:
                if self.qmData.atomicNumbers[i] == 1:
                    continue

            # set up features for node
            node = []
            
            node.append(self.qmData.atomicNumbers[i])
            node.append(self.qmData.naturalAtomicCharges[i])
            node.extend(self.qmData.naturalElectronConfiguration[i])

            # add lone pair data if available
            # otherwise set values to 0
            if i in lonePairAtomIndices:
                listIndex = lonePairAtomIndices.index(i)
                node.append(self.qmData.lonePairData[listIndex][1])
                node.extend(self.qmData.lonePairData[listIndex][2])
            else:
                node.extend([0,0,0,0,0])

            # add lone pair data if available
            # otherwise set values to 0
            if i in loneVacancyAtomIndices:
                listIndex = loneVacancyAtomIndices.index(i)
                node.append(self.qmData.loneVacancyData[listIndex][1])
                node.extend(self.qmData.loneVacancyData[listIndex][2])
            else:
                node.extend([0,0,0,0,0])

            # add implicit hydrogens
            if self.hydrogenMode == HydrogenMode.Implicit:
                node.append(hydrogenCounts[i])

            # append fully featurised node to nodes list
            nodes.append(node)
        
        # TODO normalization along features (?)

        return nodes

    def determineHydrogenCount(self, atomIndex):

        # checking Wiberg bond index matrix for bound hydrogens
        hydrogenCount = 0
        for i in range(len(self.qmData.wibergIndexMatrix[atomIndex])):

            # look for hydrogens
            if self.qmData.atomicNumbers[i] == 1:

                # check whether hydrogen has high enough bond index
                if self.qmData.wibergIndexMatrix[atomIndex][i] > self.wibergHydrogenCountThreshold:
                    hydrogenCount += 1

        return hydrogenCount

    def validateNodeList(self, nodes):
        
        # check that all node vectors have the same length
        for i in range(1, len(nodes), 1):
            assert len(nodes[i]) == len(nodes[0])
    
    def validateEdgeList(self, edges, nNodes):

        for i in range(0, len(edges), 1):
            
            # check that all edges are defined by two atom indices
            assert len(edges[i][0]) == 2
            # check that the edge defining atom indices are different
            assert edges[i][0][0] != edges[i][0][1]
            # check that all edges have feature vectors of the same length
            assert len(edges[0][1]) == len(edges[i][1])
            # check that the edge index identifier are within the range of the number of atoms
            assert edges[i][0][0] < nNodes
            assert edges[i][0][1] < nNodes
