import warnings

from Graph import Graph
from QmData import QmData
from QmAttribute import QmAttribute
from HydrogenMode import HydrogenMode

class GraphGenerator:

    """Class to generate appropriate graphs based on supplied QM data."""

    def __init__(self, attributesToExtract=[], wibergBondThreshold=0.3, wibergHydrogenCountThreshold=None, hydrogenMode=HydrogenMode.Explicit):
        """Constructor

        Args:
            attributesToExtract (list[QmAttribute]): List of attributes defining which QM properties should be extracted as attributes.
            wibergBondThreshold (float): Threshold value defining the lower bound for considering bonds.
            wibergHydrogenCountThreshold(float): Threshold value defining the lower bound for considering hydrogens as bound for implicit mode.
            hydrogenMode (HydrogenMode): Operation mode defining the way to handle hydrogens.
        """

        self.attributesToExtract = attributesToExtract

        self.wibergBondThreshold = wibergBondThreshold
        self.hydrogenMode = hydrogenMode
        self.wibergHydrogenCountThreshold = wibergHydrogenCountThreshold

        # set threshold to general bond threshold if not specified
        if wibergHydrogenCountThreshold == None:
            self.wibergHydrogenCountThreshold = self.wibergBondThreshold

    def generateGraph(self, qmData: QmData):

        # get edges
        nodes = self._getNodes(qmData)
        # check validity of nodes
        self._validateNodeList(nodes)

        # get edges
        edges = self._getEdges(qmData)
        # check validity of edges
        self._validateEdgeList(edges, len(nodes))

        # get attributes
        attributes = self._getAttributes(qmData)

        return Graph(nodes, edges, attributes)

    def _getAttributes(self, qmData: QmData):

        # return variable
        attributeList = []

        for i in range(len(self.attributesToExtract)):

            if type(self.attributesToExtract[i]) is not QmAttribute:
                warnings.warn('Element ' + str(i) + ' of list is not of type QmAttribute. Entry will be skipped.')

            if self.attributesToExtract[i] == QmAttribute.SvpElectronicEnergy:
                attributeList.append(qmData.svpElectronicEnergy)
            elif self.attributesToExtract[i] == QmAttribute.TzvpElectronicEnergy:
                attributeList.append(qmData.tzvpElectronicEnergy)
            elif self.attributesToExtract[i] == QmAttribute.SvpDispersionEnergy:
                attributeList.append(qmData.svpDispersionEnergy)
            elif self.attributesToExtract[i] == QmAttribute.TzvpDispersionEnergy:
                attributeList.append(qmData.tzvpDispersionEnergy)
            elif self.attributesToExtract[i] == QmAttribute.SvpDipoleMoment:
                attributeList.append(qmData.svpDipoleMoment)
            elif self.attributesToExtract[i] == QmAttribute.TzvpDipoleMoment:
                attributeList.append(qmData.tzvpDipoleMoment)
            elif self.attributesToExtract[i] == QmAttribute.SvpHomoEnergy:
                attributeList.append(qmData.svpHomoEnergy)
            elif self.attributesToExtract[i] == QmAttribute.TzvpHomoEnergy:
                attributeList.append(qmData.tzvpHomoEnergy)
            elif self.attributesToExtract[i] == QmAttribute.SvpLumoEnergy:
                attributeList.append(qmData.svpLumoEnergy)
            elif self.attributesToExtract[i] == QmAttribute.TzvpLumoEnergy:
                attributeList.append(qmData.tzvpLumoEnergy)
            elif self.attributesToExtract[i] == QmAttribute.SvpHomoLumoGap:
                attributeList.append(qmData.svpHomoLumoGap)
            elif self.attributesToExtract[i] == QmAttribute.TzvpHomoLumoGap:
                attributeList.append(qmData.tzvpHomoLumoGap)
            elif self.attributesToExtract[i] == QmAttribute.LowestVibrationalFrequency:
                attributeList.append(qmData.lowestVibrationalFrequency)
            elif self.attributesToExtract[i] == QmAttribute.HighestVibrationalFrequency:
                attributeList.append(qmData.highestVibrationalFrequency)
            elif self.attributesToExtract[i] == QmAttribute.HeatCapacity:
                attributeList.append(qmData.heatCapacity)
            elif self.attributesToExtract[i] == QmAttribute.Entropy:
                attributeList.append(qmData.entropy)
            elif self.attributesToExtract[i] == QmAttribute.ZpeCorrection:
                attributeList.append(qmData.zpeCorrection)
            elif self.attributesToExtract[i] == QmAttribute.EnthalpyEnergy:
                attributeList.append(qmData.enthalpyEnergy)
            elif self.attributesToExtract[i] == QmAttribute.GibbsEnergy:
                attributeList.append(qmData.gibbsEnergy)
            elif self.attributesToExtract[i] == QmAttribute.CorrectedEnthalpyEnergy:
                attributeList.append(qmData.correctedEnthalpyEnergy)
            elif self.attributesToExtract[i] == QmAttribute.CorrectedGibbsEnergy:
                attributeList.append(qmData.correctedGibbsEnergy)
            elif self.attributesToExtract[i] == QmAttribute.ElectronicEnergyDelta:
                attributeList.append(qmData.electronicEnergyDelta)
            elif self.attributesToExtract[i] == QmAttribute.DispersionEnergyDelta:
                attributeList.append(qmData.dispersionEnergyDelta)
            elif self.attributesToExtract[i] == QmAttribute.DipoleMomentDelta:
                attributeList.append(qmData.dipoleMomentDelta)
            elif self.attributesToExtract[i] == QmAttribute.HomoLumoGapDelta:
                attributeList.append(qmData.homoLumoGapDelta)
            else:
                warnings.warn('Could not find attritubte' + str(self.attributesToExtract[i]) + '.')

        return attributeList

    def _getEdges(self, qmData: QmData):

        # pre read data for efficiency
        bondPairAtomIndices = [x[0] for x in qmData.bondPairData]

        edges = []
        # iterate over half triangle matrix to determine bonds
        for i in range(len(qmData.wibergIndexMatrix) - 1):
            for j in range(i + 1, len(qmData.wibergIndexMatrix), 1):
                
                # if larger than threshold --> add bond
                if qmData.wibergIndexMatrix[i][j] > self.wibergBondThreshold:
                   
                    # append the atom indices (pos 0)
                    # and Wiberg bond index as a feature (pos 1)

                    # add all hydrogens in explicit mode
                    if self.hydrogenMode == HydrogenMode.Explicit:
                        edges.append([[i, j], [qmData.wibergIndexMatrix[i][j]]])
                    # ignore hydrogens in omit and implicit mode
                    elif self.hydrogenMode == HydrogenMode.Omit or self.hydrogenMode == HydrogenMode.Implicit:
                        if qmData.atomicNumbers[i] == 1 or qmData.atomicNumbers[j] == 1:
                            continue
                        else:
                            edges.append([[i, j], [qmData.wibergIndexMatrix[i][j]]])

        # rescale node referenes in edges if explicit hydrogens were omitted
        if self.hydrogenMode == HydrogenMode.Omit or self.hydrogenMode == HydrogenMode.Implicit:
            # get list of indices in use
            bondAtomIndices = list(set([item for sublist in [x[0] for x in edges] for item in sublist]))
            bondAtomIndices.sort()
            # loop through edges and replace node references
            for i in range(len(edges)):
                # edges[i][0][0] = bondAtomIndices.index(edges[i][0][0])
                # edges[i][0][1] = bondAtomIndices.index(edges[i][0][1])
                edges[i][0][0] = edges[i][0][0] - self._determineHydrogenPositionOffset(edges[i][0][0], qmData)
                edges[i][0][1] = edges[i][0][1] - self._determineHydrogenPositionOffset(edges[i][0][1], qmData)


        # add additional (NBO) features to edges
        for i in range(len(edges)):
            
            # check if NBO data for the respective bond is available
            # if so add to feature vector
            # otherwise add zeros to feature vector
            if edges[i][0] in bondPairAtomIndices:
                bondPairIndex = bondPairAtomIndices.index(edges[i][0])
                edges[i][1].extend(qmData.bondPairData[bondPairIndex][1])
            else:
                edges[i][1].extend([0,0,0,0])

        return edges

    def _determineHydrogenPositionOffset(self, atomIndex: int, qmData: QmData):
        
        """Counts how many hydrogen atoms are in front of (index-wise) the atom of specified index.

        Returns:
            int: The number of hydrogens in front of the atom.
        """

        hydrogenOffsetCount = 0

        # iterate through atomic numbers up to atom index
        for i in range(0, atomIndex, 1):
            if qmData.atomicNumbers[i] == 1:
                hydrogenOffsetCount += 1

        return hydrogenOffsetCount

    def _getNodes(self, qmData: QmData):

        """Gets a list of feature vectors for all nodes.

        Returns:
            list[list[floats]]: List of feature vectors of nodes.
        """

        # pre read data for efficiency
        lonePairAtomIndices = [x[0] for x in qmData.lonePairData]
        loneVacancyAtomIndices = [x[0] for x in qmData.loneVacancyData]

        # get hydrogen counts for heavy atoms in implicit mode
        hydrogenCounts = []
        if self.hydrogenMode == HydrogenMode.Implicit:
            for i in range(qmData.nAtoms):
                # skip hydrogens
                if qmData.atomicNumbers[i] == 1:
                    hydrogenCounts.append(0)
                else:
                    # determine hydrogen count
                    hydrogenCounts.append(self._determineHydrogenCount(i, qmData))

        nodes = []
        for i in range(qmData.nAtoms):

            # skip if hydrogen mode is not explicit
            if self.hydrogenMode == HydrogenMode.Omit or self.hydrogenMode == HydrogenMode.Implicit:
                if qmData.atomicNumbers[i] == 1:
                    continue

            # set up features for node
            node = []
            
            node.append(qmData.atomicNumbers[i])
            node.append(qmData.naturalAtomicCharges[i])
            node.extend(qmData.naturalElectronConfiguration[i])

            # add lone pair data if available
            # otherwise set values to 0
            if i in lonePairAtomIndices:
                listIndex = lonePairAtomIndices.index(i)
                node.append(qmData.lonePairData[listIndex][1])
                node.extend(qmData.lonePairData[listIndex][2])
            else:
                node.extend([0,0,0,0,0])

            # add lone pair data if available
            # otherwise set values to 0
            if i in loneVacancyAtomIndices:
                listIndex = loneVacancyAtomIndices.index(i)
                node.append(qmData.loneVacancyData[listIndex][1])
                node.extend(qmData.loneVacancyData[listIndex][2])
            else:
                node.extend([0,0,0,0,0])

            # add implicit hydrogens
            if self.hydrogenMode == HydrogenMode.Implicit:
                node.append(hydrogenCounts[i])

            # append fully featurised node to nodes list
            nodes.append(node)
        
        # TODO normalization along features (?)

        return nodes

    def _determineHydrogenCount(self, atomIndex: int, qmData: QmData):

        # checking Wiberg bond index matrix for bound hydrogens
        hydrogenCount = 0
        for i in range(len(qmData.wibergIndexMatrix[atomIndex])):

            # look for hydrogens
            if qmData.atomicNumbers[i] == 1:

                # check whether hydrogen has high enough bond index
                if qmData.wibergIndexMatrix[atomIndex][i] > self.wibergHydrogenCountThreshold:
                    hydrogenCount += 1

        return hydrogenCount

    def _validateNodeList(self, nodes):
        
        # check that all node vectors have the same length
        for i in range(1, len(nodes), 1):
            assert len(nodes[i]) == len(nodes[0])
    
    def _validateEdgeList(self, edges, nNodes):

        for i in range(0, len(edges), 1):
            
            # check that all edges are defined by two atom indices
            assert len(edges[i][0]) == 2
            # check that the edge defining atom indices are different
            assert edges[i][0][0] != edges[i][0][1]
            # check that all edges have feature vectors of the same length
            assert len(edges[0][1]) == len(edges[i][1])
            # check that the edge index identifiers are within the range of the number of atoms
            assert edges[i][0][0] < nNodes
            assert edges[i][0][1] < nNodes
