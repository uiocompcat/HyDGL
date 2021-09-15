from QmData import QmData
from HydrogenMode import HydrogenMode

class GraphGenerator:

    """Class to generate appropriate graphs based on supplied QM data."""

    def __init__(self, qmData):
        """Constructor

        Args:
            qmData (QmData): QmData object that holds all of the extracted QM data.
        """
        self.qmData = qmData

        # TODO these are parameters that need to be adaptable
        self.wibergBondThreshold = 0.1
        self.hydrogenMode = HydrogenMode.Implicit

    def generateGraph(self):


        edges = self.getEdges()

        nodes = self.getNodes()

        # check validity of nodes
        self.validateNodeList(nodes)
        # check validity of edges
        self.validateEdgeList(edges)
        #print(nodes)

        print(edges)

        return 0

    def getEdges(self):

        # pre read data for efficiency
        bondPairAtomIndeces = [x[0] for x in self.qmData.bondPairData]

        edges = []
        # iterate over half triangle matrix to determine bonds
        for i in range(len(self.qmData.wibergIndexMatrix) - 1):
            for j in range(i + 1, len(self.qmData.wibergIndexMatrix), 1):
                
                # if larger than threshold --> add bond
                if self.qmData.wibergIndexMatrix[i][j] > self.wibergBondThreshold:
                    # append the atom indeces (pos 0)
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


        # add additional (NBO) features to edges
        for i in range(len(edges)):
            
            # check if NBO data for the respective bond is available
            # if so add to feature vector
            # otherwise add zeros to feature vector
            if edges[i][0] in bondPairAtomIndeces:
                bondPairIndex = bondPairAtomIndeces.index(edges[i][0])
                edges[i][1].extend(self.qmData.bondPairData[bondPairIndex][1])
            else:
                edges[i][1].extend([0,0,0,0])

        return edges

    def getNodes(self):

        # pre read data for efficiency
        lonePairAtomIndeces = [x[0] for x in self.qmData.lonePairData]
        loneVacancyAtomIndeces = [x[0] for x in self.qmData.loneVacancyData]

        # get hydrogen counts for heavy atoms in implicit mode
        hydrogenCounts = []
        if self.hydrogenMode == HydrogenMode.Implicit:
            for i in range(self.qmData.nAtoms):
                # skip hydrogens
                if self.qmData.atomicNumber[i] == 1:
                    continue
                    
                

        nodes = []
        for i in range(self.qmData.nAtoms):

            # skip if hydrogen mode is note explicit
            if self.hydrogenMode == HydrogenMode.Omit or self.hydrogenMode == HydrogenMode.Implicit:
                if self.qmData.atomicNumber[i] == 1:
                    continue

            # set up features for node
            node = []
            
            node.append(self.qmData.atomicNumbers[i])
            node.append(self.qmData.naturalAtomicCharges[i])
            node.extend(self.qmData.naturalElectronConfiguration[i])

            # add lone pair data if available
            # otherwise set values to 0
            if i in lonePairAtomIndeces:
                listIndex = lonePairAtomIndeces.index(i)
                node.append(self.qmData.lonePairData[listIndex][1])
                node.extend(self.qmData.lonePairData[listIndex][2])
            else:
                node.extend([0,0,0,0,0])

            # add lone pair data if available
            # otherwise set values to 0
            if i in loneVacancyAtomIndeces:
                listIndex = loneVacancyAtomIndeces.index(i)
                node.append(self.qmData.loneVacancyData[listIndex][1])
                node.extend(self.qmData.loneVacancyData[listIndex][2])
            else:
                node.extend([0,0,0,0,0])

            if self.hydrogenMode == HydrogenMode.Implicit:
                print(1)

            # append fully featurised node to nodes list
            nodes.append(node)
        
        # TODO normalization along features (?)

        return nodes

    def validateNodeList(self, nodes):
        
        # check that there are as many nodes as atoms in the system
        assert len(nodes) == self.qmData.nAtoms

        # check that all node vectors have the same length
        for i in range(1, len(nodes), 1):
            assert len(nodes[i]) == len(nodes[0])
    
    def validateEdgeList(self, edges):

        # check that all edges are defined by two atom indeces
        # check that all edges have feature vectors of the same length
        for i in range(1, len(edges), 1):

            assert len(edges[0][0]) == len(edges[i][0])
            assert len(edges[0][1]) == len(edges[i][1])
        
