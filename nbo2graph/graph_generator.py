from torch._C import Node
import warnings

from nbo2graph.graph import Graph
from nbo2graph.qm_data import QmData
from nbo2graph.qm_atrribute import QmAttribute
from nbo2graph.edge_feature import EdgeFeature
from nbo2graph.node_feature import NodeFeature
from nbo2graph.hydrogen_mode import HydrogenMode
from nbo2graph.bond_determination_mode import BondDeterminationMode

class GraphGenerator:

    """Class to generate appropriate graphs based on supplied QM data."""

    def __init__(self, node_features: list[NodeFeature] = [],
                       edge_feautres: list[EdgeFeature] = [],
                       attributes_to_extract: list[QmAttribute] =[],
                       bond_determination_mode: BondDeterminationMode = BondDeterminationMode.WIBERG,
                       bond_threshold=0.3, 
                       hydrogen_count_threshold=0.5, 
                       hydrogen_mode=HydrogenMode.EXPLICIT):
        """Constructor

        Args:
            node_features (list[NodeFeature]): List of node features to extract.
            edge_features (list[EdgeFeature]): List of edge features to extract.
            bond_determination_mode (BondDeterminationMode): Specifies the way bonds are determined when building the graph.
            attributes_to_extract (list[QmAttribute]): List of attributes defining which QM properties should be extracted as attributes.
            bond_threshold (float): Threshold value defining the lower bound for considering bonds.
            hydrogen_count_threshold(float): Threshold value defining the lower bound for considering hydrogens as bound for implicit mode.
            hydrogen_mode (HydrogenMode): Operation mode defining the way to handle hydrogens.
        """

        self.node_features = node_features
        self.edge_features = edge_feautres

        self.bond_determination_mode = bond_determination_mode

        self.attributes_to_extract = attributes_to_extract

        self.bond_threshold = bond_threshold
        self.hydrogen_mode = hydrogen_mode
        self.hydrogen_count_threshold = hydrogen_count_threshold

    def generate_graph(self, qm_data: QmData):

        # get edges
        nodes = self._get_nodes(qm_data)
        # check validity of nodes
        self._validate_node_list(nodes)

        # get edges
        edges = self._get_edges(qm_data)
        # check validity of edges
        self._validate_edge_list(edges, len(nodes))

        # get attributes
        attributes = self._get_attributes(qm_data)

        return Graph(nodes, edges, attributes)

    def _get_attributes(self, qm_data: QmData):

        # return variable
        attribute_list = []

        for i in range(len(self.attributes_to_extract)):

            if type(self.attributes_to_extract[i]) is not QmAttribute:
                warnings.warn('Element ' + str(i) + ' of list is not of type QmAttribute. Entry will be skipped.')

            if self.attributes_to_extract[i] == QmAttribute.SVP_ELECTRONIC_ENERGY:
                attribute_list.append(qm_data.svp_electronic_energy)
            elif self.attributes_to_extract[i] == QmAttribute.TZVP_ELECTRONIC_ENERGY:
                attribute_list.append(qm_data.tzvp_electronic_energy)
            elif self.attributes_to_extract[i] == QmAttribute.SVP_DISPERSION_ENERGY:
                attribute_list.append(qm_data.svp_dispersion_energy)
            elif self.attributes_to_extract[i] == QmAttribute.TZVP_DISPERSION_ENERGY:
                attribute_list.append(qm_data.tzvp_dispersion_energy)
            elif self.attributes_to_extract[i] == QmAttribute.SVP_DIPOLE_MOMENT:
                attribute_list.append(qm_data.svp_dipole_moment)
            elif self.attributes_to_extract[i] == QmAttribute.TZVP_DIPOLE_MOMENT:
                attribute_list.append(qm_data.tzvp_dipole_moment)
            elif self.attributes_to_extract[i] == QmAttribute.SVP_HOMO_ENERGY:
                attribute_list.append(qm_data.svp_homo_energy)
            elif self.attributes_to_extract[i] == QmAttribute.TZVP_HOMO_ENERGY:
                attribute_list.append(qm_data.tzvp_homo_energy)
            elif self.attributes_to_extract[i] == QmAttribute.SVP_LUMO_ENERGY:
                attribute_list.append(qm_data.svp_lumo_energy)
            elif self.attributes_to_extract[i] == QmAttribute.TZVP_LUMO_ENERGY:
                attribute_list.append(qm_data.tzvp_lumo_energy)
            elif self.attributes_to_extract[i] == QmAttribute.SVP_HOMO_LUMO_GAP:
                attribute_list.append(qm_data.svp_homo_lumo_gap)
            elif self.attributes_to_extract[i] == QmAttribute.TZVP_HOMO_LUMO_GAP:
                attribute_list.append(qm_data.tzvp_homo_lumo_gap)
            elif self.attributes_to_extract[i] == QmAttribute.LOWEST_VIBRATIONAL_FREQUENCY:
                attribute_list.append(qm_data.lowest_vibrational_frequency)
            elif self.attributes_to_extract[i] == QmAttribute.HIGHEST_VIBRATIONAL_FREQUENCY:
                attribute_list.append(qm_data.highest_vibrational_frequency)
            elif self.attributes_to_extract[i] == QmAttribute.HEAT_CAPACITY:
                attribute_list.append(qm_data.heat_capacity)
            elif self.attributes_to_extract[i] == QmAttribute.ENTROPY:
                attribute_list.append(qm_data.entropy)
            elif self.attributes_to_extract[i] == QmAttribute.ZPE_CORRECTION:
                attribute_list.append(qm_data.zpe_correction)
            elif self.attributes_to_extract[i] == QmAttribute.ENTHALPY_ENERGY:
                attribute_list.append(qm_data.enthalpy_energy)
            elif self.attributes_to_extract[i] == QmAttribute.GIBBS_ENERGY:
                attribute_list.append(qm_data.gibbs_energy)
            elif self.attributes_to_extract[i] == QmAttribute.CORRECTED_ENTHALPY_ENERGY:
                attribute_list.append(qm_data.corrected_enthalpy_energy)
            elif self.attributes_to_extract[i] == QmAttribute.CORRECTED_GIBBS_ENERGY:
                attribute_list.append(qm_data.corrected_gibbs_energy)
            elif self.attributes_to_extract[i] == QmAttribute.ELECTRONIC_ENERGY_DELTA:
                attribute_list.append(qm_data.electronic_energy_delta)
            elif self.attributes_to_extract[i] == QmAttribute.DISPERSION_ENERGY_DELTA:
                attribute_list.append(qm_data.dispersion_energy_delta)
            elif self.attributes_to_extract[i] == QmAttribute.DIPOLE_MOMENT_DELTA:
                attribute_list.append(qm_data.dipole_moment_delta)
            elif self.attributes_to_extract[i] == QmAttribute.HOMO_LUMO_GAP_DELTA:
                attribute_list.append(qm_data.homo_lumo_gap_delta)
            else:
                warnings.warn('Could not find attritubte' + str(self.attributes_to_extract[i]) + '.')

        return attribute_list

    def _get_edges(self, qm_data: QmData):

        # pre read data for efficiency

        # bonds with BD and BD*
        bond_pair_atom_indices = [x[0] for x in qm_data.bond_pair_data_full]
        antibond_pair_atom_indices = [x[0] for x in qm_data.antibond_pair_data_full]

        # corresponding energy values
        bond_pair_energies = [x[1] for x in qm_data.bond_pair_data_full]
        antibond_pair_energies = [x[1] for x in qm_data.antibond_pair_data_full]

        # decide which index matrix to use
        index_matrix = None
        # Wiberg mode
        if self.bond_determination_mode == BondDeterminationMode.WIBERG:
            index_matrix = qm_data.wiberg_index_matrix
        # LMO mode
        elif self.bond_determination_mode == BondDeterminationMode.LMO:
            index_matrix = qm_data.lmo_bond_order_matrix
        # NLMO mode
        elif self.bond_determination_mode == BondDeterminationMode.NLMO:
            index_matrix = qm_data.nbo_bond_order_matrix
        
        edges = []
        # iterate over half triangle matrix to determine bonds
        for i in range(len(index_matrix) - 1):
            for j in range(i + 1, len(index_matrix), 1):

                # if larger than threshold --> add bond
                if (index_matrix[i][j]) > self.bond_threshold:
                
                    # append the atom indices (pos 0)
                    # and Wiberg bond index as a feature (pos 1)

                    # ignore hydrogens in omit and implicit mode
                    if self.hydrogen_mode == HydrogenMode.OMIT or self.hydrogen_mode == HydrogenMode.IMPLICIT:
                        if qm_data.atomic_numbers[i] == 1 or qm_data.atomic_numbers[j] == 1:
                            continue
                    
                    # append edge with empty feature vector
                    edges.append([[i, j], []])

                    # append bond order as feature if requested
                    if EdgeFeature.BOND_ORDER in self.edge_features:
                        edges[-1][1].append(index_matrix[i][j])
    
                
        # add additional (NBO) features to edges
        for i in range(len(edges)):             

            if EdgeFeature.BOND_DISTANCE in self.edge_features:
                # add bond distance as feature to edges
                edges[i][1].append(qm_data.bond_distance_matrix[edges[i][0][0]][edges[i][0][1]])

            if EdgeFeature.BOND_ORBITAL_DATA in self.edge_features:
                # check if NBO data for the respective bond is available
                # if so add to feature vector
                # otherwise add zeros to feature vector
                if edges[i][0] in bond_pair_atom_indices:

                    # get list of all lone pair energies for this atom
                    energies = [x[1] for x in qm_data.bond_pair_data_full if x[0] == edges[i][0]]

                    # select index of the highest energy (for BD)
                    selected_index = bond_pair_energies.index(max(energies))

                    # append data (total length = 6)
                    edges[i][1].append(len(energies))
                    edges[i][1].append(qm_data.bond_pair_data_full[selected_index][1])
                    edges[i][1].append(qm_data.bond_pair_data_full[selected_index][2])
                    edges[i][1].extend(qm_data.bond_pair_data_full[selected_index][3][:3]) # only consider s, p and d orbitals
                else:
                    edges[i][1].extend([0,0,0,0,0,0])

            if EdgeFeature.ANTIBOND_ORBITAL_DATA in self.edge_features:
                # check if NBO data for the respective antibonds is available
                # if so add to feature vector
                # otherwise add zeros to feature vector
                if edges[i][0] in antibond_pair_atom_indices:

                    # get list of all lone pair energies for this atom
                    energies = [x[1] for x in qm_data.antibond_pair_data_full if x[0] == edges[i][0]]

                    # select index of the lowest energy (for BD*)
                    selected_index = antibond_pair_energies.index(min(energies))

                    # append data (total length = 5)
                    # edges[i][1].append(len(energies)) # omitted since number of antibonds same to number of bonds
                    edges[i][1].append(qm_data.antibond_pair_data_full[selected_index][1])  
                    edges[i][1].append(qm_data.antibond_pair_data_full[selected_index][2])
                    edges[i][1].extend(qm_data.antibond_pair_data_full[selected_index][3][:3]) # only consider s, p and d orbitals
                else:
                    edges[i][1].extend([0,0,0,0,0])

        # rescale node referenes in edges if explicit hydrogens were omitted
        if self.hydrogen_mode == HydrogenMode.OMIT or self.hydrogen_mode == HydrogenMode.IMPLICIT:
            # get list of indices in use
            bond_atom_indices = list(set([item for sublist in [x[0] for x in edges] for item in sublist]))
            bond_atom_indices.sort()
            # loop through edges and replace node references
            for i in range(len(edges)):
                edges[i][0][0] = edges[i][0][0] - self._determine_hydrogen_position_offset(edges[i][0][0], qm_data)
                edges[i][0][1] = edges[i][0][1] - self._determine_hydrogen_position_offset(edges[i][0][1], qm_data)

        return edges

    def _get_nodes(self, qm_data: QmData):

        """Gets a list of feature vectors for all nodes.

        Returns:
            list[list[floats]]: List of feature vectors of nodes.
        """

        # get hydrogen counts for heavy atoms in implicit mode
        hydrogen_counts = []
        if self.hydrogen_mode == HydrogenMode.IMPLICIT:
            for i in range(qm_data.n_atoms):
                # skip hydrogens
                if qm_data.atomic_numbers[i] == 1:
                    hydrogen_counts.append(0)
                else:
                    # determine hydrogen count
                    hydrogen_counts.append(self._determine_hydrogen_count(i, qm_data))

        nodes = []
        for i in range(qm_data.n_atoms):

            # skip if hydrogen mode is not explicit
            if self.hydrogen_mode == HydrogenMode.OMIT or self.hydrogen_mode == HydrogenMode.IMPLICIT:
                if qm_data.atomic_numbers[i] == 1:
                    continue

            node = self._get_individual_node(qm_data, i)
            
            # add implicit hydrogens
            if self.hydrogen_mode == HydrogenMode.IMPLICIT:
                node.append(hydrogen_counts[i])

            # append fully featurised node to nodes list
            nodes.append(node)
        
        # TODO normalization along features (?)

        return nodes

    def _get_individual_node(self, qm_data: QmData, atom_index: int):

        # for brevity
        i = atom_index

        # pre read data for efficiency

        # atom indices that have LP or LV
        lone_pair_atom_indices = [x[0] for x in qm_data.lone_pair_data_full]
        lone_vacancy_atom_indices = [x[0] for x in qm_data.lone_vacancy_data_full]

        # corresponding energy values
        lone_pair_energies = [x[1] for x in qm_data.lone_pair_data_full]
        lone_vacancy_energies = [x[1] for x in qm_data.lone_vacancy_data_full]

        # set up features for node
        node = []
        
        if NodeFeature.ATOMIC_NUMBERS in self.node_features:
            node.append(qm_data.atomic_numbers[i])
    
        if NodeFeature.NATURAL_ATOMIC_CHARGES in self.node_features:
            node.append(qm_data.natural_atomic_charges[i])
    
        if NodeFeature.NATURAL_ELECTRON_CONFIGURATION in self.node_features:
            node.extend(qm_data.natural_electron_configuration[i])

        if NodeFeature.BOND_ORDER_TOTAL in self.node_features:
            # add bond order totals per atom
            # Wiberg mode
            if self.bond_determination_mode == BondDeterminationMode.WIBERG:
                node.append(qm_data.wiberg_atom_totals[i])
            # LMO mode
            elif self.bond_determination_mode == BondDeterminationMode.LMO:
                node.append(qm_data.nbo_bond_order_totals[i])        
            # NLMO mode
            elif self.bond_determination_mode == BondDeterminationMode.NLMO:
                node.append(qm_data.nbo_bond_order_totals[i])
            else:
                warnings.warn('Bond determination mode ' + str(self.bond_determination_mode) + ' not recognised. Skipping')

        if NodeFeature.LONE_PAIRS in self.node_features:
            # add lone pair data if available
            # otherwise set values to 0
            if i in lone_pair_atom_indices:

                # get list of all lone pair energies for this atom
                energies = [x[1] for x in qm_data.lone_pair_data_full if x[0] == i]
                # select index of the highest energy (for LP)
                selected_index = lone_pair_energies.index(max(energies))

                # append data (total length = 5)
                node.append(len(energies))
                node.append(qm_data.lone_pair_data_full[selected_index][1])
                node.append(qm_data.lone_pair_data_full[selected_index][2])

                # get only s and d symmetries
                oribtal_symmetries = [qm_data.lone_pair_data_full[selected_index][3][k] for k in [0,2]]
                node.extend(oribtal_symmetries)
            else:
                node.extend([0,0,0,0,0])


        if NodeFeature.LONE_VACANCIES in self.node_features:
            # add lone vacancy data if available
            # otherwise set values to 0
            if i in lone_vacancy_atom_indices:

                # get list of all lone pair energies for this atom
                energies = [x[1] for x in qm_data.lone_vacancy_data_full if x[0] == i]
                # select index of the lowest energy (for LV)
                selected_index = lone_vacancy_energies.index(min(energies))

                # append data (total length = 5)
                node.append(len(energies))
                node.append(qm_data.lone_vacancy_data_full[selected_index][1])
                node.append(qm_data.lone_vacancy_data_full[selected_index][2])

                # get only s and d symmetries
                oribtal_symmetries = [qm_data.lone_vacancy_data_full[selected_index][3][k] for k in [0,2]]
                node.extend(oribtal_symmetries)
            else:
                node.extend([0,0,0,0,0])

        return node


    def _determine_hydrogen_position_offset(self, atom_index: int, qm_data: QmData):
        
        """Counts how many hydrogen atoms are in front of (index-wise) the atom of specified index.

        Returns:
            int: The number of hydrogens in front of the atom.
        """

        hydrogen_offset_count = 0

        # iterate through atomic numbers up to atom index
        for i in range(0, atom_index, 1):
            if qm_data.atomic_numbers[i] == 1:
                hydrogen_offset_count += 1

        return hydrogen_offset_count

    def _determine_hydrogen_count(self, atom_index: int, qm_data: QmData):

        """Determines how many hyrdogen atoms are bound to the atom with the specified index.

        Returns:
            int: The number of bound hydrogen atoms.
        """

        # checking Wiberg bond index matrix for bound hydrogens
        hydrogen_count = 0
        for i in range(len(qm_data.wiberg_index_matrix[atom_index])):

            # look for hydrogens
            if qm_data.atomic_numbers[i] == 1:

                # check whether hydrogen has high enough bond index
                if qm_data.wiberg_index_matrix[atom_index][i] > self.hydrogen_count_threshold:
                    hydrogen_count += 1

        return hydrogen_count

    def _validate_node_list(self, nodes):
        
        # check that all node vectors have the same length
        for i in range(1, len(nodes), 1):
            assert len(nodes[i]) == len(nodes[0])
    
    def _validate_edge_list(self, edges, n_nodes):

        for i in range(0, len(edges), 1):
            
            # check that all edges are defined by two atom indices
            assert len(edges[i][0]) == 2
            # check that the edge defining atom indices are different
            assert edges[i][0][0] != edges[i][0][1]
            # check that all edges have feature vectors of the same length
            assert len(edges[0][1]) == len(edges[i][1])
            # check that the edge index identifiers are within the range of the number of atoms
            assert edges[i][0][0] < n_nodes
            assert edges[i][0][1] < n_nodes
