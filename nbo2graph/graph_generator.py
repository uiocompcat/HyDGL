import warnings
from statistics import mean

from nbo2graph.graph import Graph
from nbo2graph.qm_data import QmData
from nbo2graph.enums.qm_target import QmTarget
from nbo2graph.enums.edge_feature import EdgeFeature
from nbo2graph.enums.node_feature import NodeFeature
from nbo2graph.enums.hydrogen_mode import HydrogenMode
from nbo2graph.enums.graph_feature import GraphFeature
from nbo2graph.element_look_up_table import ElementLookUpTable
from nbo2graph.graph_generator_settings import GraphGeneratorSettings
from nbo2graph.enums.bond_determination_mode import BondDeterminationMode


class GraphGenerator:

    """Class to generate appropriate graphs based on supplied QM data."""

    def __init__(self, settings: GraphGeneratorSettings):
        """Constructor

        Args:
            settings (GraphGeneratorSettings): Settings for GG.
        """

        self.settings = settings

    def generate_graph(self, qm_data: QmData):

        """Generates a graph according to the specified settings.

        Returns:
            Graph: The graph representation of the graph.
        """

        # get edges
        nodes = self._get_nodes(qm_data)
        # get edges
        edges = self._get_edges(qm_data)

        # rescale node referenes in edges if explicit hydrogens were omitted
        if self.settings.hydrogen_mode == HydrogenMode.OMIT or self.settings.hydrogen_mode == HydrogenMode.IMPLICIT:
            edges = self._adjust_node_references(edges, qm_data)

        # check validity of nodes
        self._validate_node_list(nodes)
        # check validity of edges
        self._validate_edge_list(edges, len(nodes))

        # get graph features
        graph_features = self._get_graph_features(qm_data)

        # get targets
        targets = self._get_targets(qm_data)

        return Graph(nodes,
                     edges,
                     id=qm_data.id,
                     stoichiometry=qm_data.stoichiometry,
                     targets=targets,
                     graph_features=graph_features)

    def _get_edges(self, qm_data: QmData):

        """Gets edges and their corresponding feature vectors.

        Returns:
            list[list[int], float]: Adjacency list with corresponding feature vectors.
        """

        # get adjacency list
        adjacency_list = self._get_adjacency_list(qm_data)

        edges = []
        # generate featurised edges
        for i in range(len(adjacency_list)):
            edges.append(self._get_featurised_edge(adjacency_list[i], qm_data))

        # operations only relevant when not modelling hydrogens explicitly
        if self.settings.hydrogen_mode == HydrogenMode.OMIT or self.settings.hydrogen_mode == HydrogenMode.IMPLICIT:

            # check for hydride hydrogens to add explicitly
            hydride_bond_indices = self._get_hydride_bond_indices(qm_data)
            for i in range(len(hydride_bond_indices)):
                edges.append(self._get_featurised_edge(hydride_bond_indices[i], qm_data))

        return edges

    def _get_adjacency_list(self, qm_data: QmData):

        # get appropriate index matrix
        index_matrix = self._get_index_matrix(qm_data)

        adjacency_list = []
        # iterate over half triangle matrix to determine bonds
        for i in range(len(index_matrix) - 1):
            for j in range(i + 1, len(index_matrix), 1):

                # if larger than threshold --> add bond
                if (index_matrix[i][j]) > self.settings.bond_threshold:

                    # append the atom indices (pos 0)
                    # and Wiberg bond index as a feature (pos 1)

                    # ignore hydrogens in omit and implicit mode
                    if self.settings.hydrogen_mode == HydrogenMode.OMIT or self.settings.hydrogen_mode == HydrogenMode.IMPLICIT:
                        if qm_data.atomic_numbers[i] == 1 or qm_data.atomic_numbers[j] == 1:
                            continue

                    # append edge with empty feature vector
                    adjacency_list.append([i, j])

        return adjacency_list

    def _get_featurised_edge(self, bond_atom_indices: list[int], qm_data: QmData):

        # pre read data for efficiency

        # bonds with BD and BD*
        bond_pair_atom_indices = [x[0] for x in qm_data.bond_pair_data_full]
        antibond_pair_atom_indices = [x[0] for x in qm_data.antibond_pair_data_full]

        # corresponding energy values
        bond_pair_energies = [x[1] for x in qm_data.bond_pair_data_full]
        antibond_pair_energies = [x[1] for x in qm_data.antibond_pair_data_full]

        # sort indices for consitency
        bond_atom_indices.sort()
        # set up variable for edge; format: [ [i,j], [feature1, feature2, ...] ]
        edge = [bond_atom_indices, []]

        # get appropriate index matrix
        index_matrix = self._get_index_matrix(qm_data)

        # append bond order as feature if requested
        if EdgeFeature.BOND_ORDER in self.settings.edge_features:
            edge[1].append(index_matrix[edge[0][0]][edge[0][1]])

        # add bond distance as feature to edges
        if EdgeFeature.BOND_DISTANCE in self.settings.edge_features:
            edge[1].append(qm_data.bond_distance_matrix[edge[0][0]][edge[0][1]])

        # add number of bond/antibond orbitals if requested
        if len(self.settings.bond_orbital_indices) > 0 or len(self.settings.antibond_orbital_indices) > 0:
            if edge[0] in bond_pair_atom_indices:

                # get list of all bond energies for this atom
                energies = [x[1] for x in qm_data.bond_pair_data_full if x[0] == edge[0]]

                edge[1].append(len(energies))
            else:
                edge[1].append(0)

        if len(self.settings.bond_orbital_indices) > 0:
            # check if NBO data for the respective bond is available
            # if so add to feature vector
            # otherwise add zeros to feature vector
            if edge[0] in bond_pair_atom_indices:

                # get list of all bond pair energies for this atom
                energies = [x[1] for x in qm_data.bond_pair_data_full if x[0] == edge[0]]

                # select index of the highest energy (for BD)
                selected_index = bond_pair_energies.index(max(energies))

                # append data (total length = 2 + number of orbital occupancies)
                edge[1].append(qm_data.bond_pair_data_full[selected_index][1])
                edge[1].append(qm_data.bond_pair_data_full[selected_index][2])
                edge[1].extend([qm_data.bond_pair_data_full[selected_index][3][k] for k in self.settings.bond_orbital_indices])

            else:
                edge[1].extend((2 + len(self.settings.bond_orbital_indices)) * [0])

        if len(self.settings.antibond_orbital_indices) > 0:
            # check if NBO data for the respective antibonds is available
            # if so add to feature vector
            # otherwise add zeros to feature vector
            if edge[0] in antibond_pair_atom_indices:

                # get list of all antibond pair energies for this atom
                energies = [x[1] for x in qm_data.antibond_pair_data_full if x[0] == edge[0]]

                # select index of the lowest energy (for BD*)
                selected_index = antibond_pair_energies.index(min(energies))

                # append data (total length = 2 + number of orbital occupancies)
                edge[1].append(qm_data.antibond_pair_data_full[selected_index][1])
                edge[1].append(qm_data.antibond_pair_data_full[selected_index][2])
                edge[1].extend([qm_data.bond_pair_data_full[selected_index][3][k] for k in self.settings.antibond_orbital_indices])
            else:
                edge[1].extend((2 + len(self.settings.antibond_orbital_indices)) * [0])

        return edge

    def _get_nodes(self, qm_data: QmData):

        """Gets a list of feature vectors for all nodes.

        Returns:
            list[list[floats]]: List of feature vectors of nodes.
        """

        nodes = []
        for i in range(qm_data.n_atoms):

            # skip if hydrogen mode is not explicit
            if self.settings.hydrogen_mode == HydrogenMode.OMIT or self.settings.hydrogen_mode == HydrogenMode.IMPLICIT:
                if qm_data.atomic_numbers[i] == 1:
                    continue

            # get ith node
            node = self._get_individual_node(qm_data, i)

            # append fully featurised node to nodes list
            nodes.append(node)

        # operations only relevant when not modelling hydrogens explicitly
        if self.settings.hydrogen_mode == HydrogenMode.OMIT or self.settings.hydrogen_mode == HydrogenMode.IMPLICIT:

            # check for hydride hydrogens to add explicitly
            hydride_bond_indices = self._get_hydride_bond_indices(qm_data)
            for i in range(len(hydride_bond_indices)):
                # get node
                node = self._get_individual_node(qm_data, hydride_bond_indices[i][0])
                # insert at correct place in node list
                nodes.insert(hydride_bond_indices[i][0], node)

        return nodes

    def _get_individual_node(self, qm_data: QmData, atom_index: int):

        """Gets the feature vector for one node.

        Returns:
            list[float]: The feature vector of the corresponding atom.
        """

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

        # add atomic number
        if NodeFeature.ATOMIC_NUMBERS in self.settings.node_features:
            node.append(qm_data.atomic_numbers[i])

        # add natural atomic charge
        if NodeFeature.NATURAL_ATOMIC_CHARGES in self.settings.node_features:
            node.append(qm_data.natural_atomic_charges[i])

        # add natural electron configuration (requested orbital occupancies)
        if len(self.settings.natural_orbital_configuration_indices) > 0:
            node.extend([qm_data.natural_electron_configuration[i][k] for k in self.settings.natural_orbital_configuration_indices])

        # add bond order totals
        if NodeFeature.BOND_ORDER_TOTAL in self.settings.node_features:
            # Wiberg mode
            if self.settings.bond_determination_mode == BondDeterminationMode.WIBERG:
                node.append(qm_data.wiberg_atom_totals[i])
            # LMO mode
            elif self.settings.bond_determination_mode == BondDeterminationMode.LMO:
                node.append(qm_data.nbo_bond_order_totals[i])
            # NLMO mode
            elif self.settings.bond_determination_mode == BondDeterminationMode.NLMO:
                node.append(qm_data.nbo_bond_order_totals[i])
            else:
                warnings.warn('Bond determination mode ' + str(self.settings.bond_determination_mode) + ' not recognised. Skipping')

        # add lone pair data if requested
        if (NodeFeature.LONE_PAIR_MAX in self.settings.node_features or NodeFeature.LONE_PAIR_AVERAGE in self.settings.node_features) \
                and len(self.settings.lone_pair_orbital_indices) > 0:

            # get list of all lone pair energies for this atom
            energies = [x[1] for x in qm_data.lone_pair_data_full if x[0] == i]
            # append number of lone pair as feature
            node.append(len(energies))

            if NodeFeature.LONE_PAIR_MAX in self.settings.node_features:
                if i in lone_pair_atom_indices:

                    # select index of the highest energy (for LP)
                    selected_index = lone_pair_energies.index(max(energies))

                    # append data (total length = 4)
                    node.append(qm_data.lone_pair_data_full[selected_index][1])
                    node.append(qm_data.lone_pair_data_full[selected_index][2])

                    # get orbital occupations
                    oribtal_symmetries = [qm_data.lone_pair_data_full[selected_index][3][k] for k in self.settings.lone_pair_orbital_indices]
                    node.extend(oribtal_symmetries)
                else:
                    node.extend((2 + len(self.settings.lone_pair_orbital_indices)) * [0])

            if NodeFeature.LONE_PAIR_AVERAGE in self.settings.node_features:
                if i in lone_pair_atom_indices:

                    # get list of all lone pair occupations for this atom
                    occupations = [x[2] for x in qm_data.lone_pair_data_full if x[0] == i]
                    # get list of symmetry values of different lone pairs for this atom
                    symmetries = [x[3] for x in qm_data.lone_pair_data_full if x[0] == i]

                    # append average values for energies and occupations
                    node.append(mean(energies))
                    node.append(mean(occupations))

                    # get average values for orbital symmetries
                    oribtal_symmetries = [mean(x) for x in [[y[k] for y in symmetries] for k in self.settings.lone_pair_orbital_indices]]
                    node.extend(oribtal_symmetries)
                else:
                    node.extend((2 + len(self.settings.lone_pair_orbital_indices)) * [0])

        # add lone vacancy data if requested
        if (NodeFeature.LONE_VACANCY_MIN in self.settings.node_features or NodeFeature.LONE_VACANCY_AVERAGE in self.settings.node_features) \
                and len(self.settings.lone_vacancy_orbital_indices) > 0:

            # get list of all lone pair energies for this atom
            energies = [x[1] for x in qm_data.lone_vacancy_data_full if x[0] == i]
            node.append(len(energies))

            if NodeFeature.LONE_VACANCY_MIN in self.settings.node_features:
                if i in lone_vacancy_atom_indices:

                    # select index of the lowest energy (for LV)
                    selected_index = lone_vacancy_energies.index(min(energies))

                    # append data (total length = 4)
                    node.append(qm_data.lone_vacancy_data_full[selected_index][1])
                    node.append(qm_data.lone_vacancy_data_full[selected_index][2])

                    # get orbital occupations
                    oribtal_symmetries = [qm_data.lone_vacancy_data_full[selected_index][3][k] for k in self.settings.lone_vacancy_orbital_indices]
                    node.extend(oribtal_symmetries)
                else:
                    node.extend((2 + len(self.settings.lone_vacancy_orbital_indices)) * [0])

            if NodeFeature.LONE_VACANCY_AVERAGE in self.settings.node_features:
                if i in lone_vacancy_atom_indices:

                    # get list of all lone pair occupations for this atom
                    occupations = [x[2] for x in qm_data.lone_vacancy_data_full if x[0] == i]
                    # get list of symmetry values of different lone pairs for this atom
                    symmetries = [x[3] for x in qm_data.lone_vacancy_data_full if x[0] == i]

                    # append average values for energies and occupations
                    node.append(mean(energies))
                    node.append(mean(occupations))

                    # get average values for orbital symmetries
                    oribtal_symmetries = [mean(x) for x in [[y[k] for y in symmetries] for k in self.settings.lone_vacancy_orbital_indices]]
                    node.extend(oribtal_symmetries)
                else:
                    node.extend((2 + len(self.settings.lone_vacancy_orbital_indices)) * [0])

        # add implicit hydrogens
        if self.settings.hydrogen_mode == HydrogenMode.IMPLICIT:
            # get hydrogen count for heavy atoms in implicit mode
            hydrogen_count = None
            if self.settings.hydrogen_mode == HydrogenMode.IMPLICIT:
                # set hydrogen count of hydrogens to 0
                if qm_data.atomic_numbers[i] == 1:
                    hydrogen_count = 0
                # set hydrogen count to 0 if transition metal (will be modelled explicitly)
                elif qm_data.atomic_numbers[i] in ElementLookUpTable.transition_metal_atomic_numbers:
                    hydrogen_count = 0
                # otherwise determine hydrogen count normally
                else:
                    hydrogen_count = self._determine_hydrogen_count(i, qm_data)

            node.append(hydrogen_count)

        return node

    def _adjust_node_references(self, edges, qm_data: QmData):

        """Rescales the node references for implicit/omit mode where hydrogens are not explicit nodes (except hydride hydrogens).

        Returns:
            list[list[int], list[float]]: Edges list with rescaled node references.
        """

        # get list of indices in use
        bond_atom_indices = list(set([item for sublist in [x[0] for x in edges] for item in sublist]))
        bond_atom_indices.sort()
        # loop through edges and replace node references
        for i in range(len(edges)):
            edges[i][0][0] = edges[i][0][0] - self._determine_hydrogen_position_offset(edges[i][0][0], qm_data)
            edges[i][0][1] = edges[i][0][1] - self._determine_hydrogen_position_offset(edges[i][0][1], qm_data)

        return edges

    def _determine_hydrogen_position_offset(self, atom_index: int, qm_data: QmData):

        """Counts how many hydrogen atoms are in front of (index-wise) the atom of specified index.

        Returns:
            int: The number of hydrogens in front of the atom.
        """

        # get list of hydride hydrogen indices
        hydride_hydrogen_indices = self._get_hydride_hydrogen_indices(qm_data)

        hydrogen_offset_count = 0

        # iterate through atomic numbers up to atom index
        for i in range(0, atom_index, 1):
            if qm_data.atomic_numbers[i] == 1:
                # check if hydrogen is a hydrite hydrogen
                # only increment if hydrogen is not a hydride hydrogen
                if i not in hydride_hydrogen_indices:
                    hydrogen_offset_count += 1

        return hydrogen_offset_count

    def _get_hydride_hydrogen_indices(self, qm_data: QmData):

        """Returns a list of hydride hydrogen indices.

        Returns:
            list[int]: List of hydride hydrogen indices
        """

        # return variable
        hydride_hydrogen_indices = []

        for i in range(len(qm_data.atomic_numbers)):

            # look for transition metals
            if qm_data.atomic_numbers[i] in ElementLookUpTable.transition_metal_atomic_numbers:
                # get bound h atom indices and append to return variable
                hydride_hydrogen_indices.extend(self._get_bound_h_atom_indices(i, qm_data, threshold=self.settings.hydrogen_count_threshold))

        return hydride_hydrogen_indices

    def _get_hydride_bond_indices(self, qm_data: QmData):

        """Returns a list of hydride bonds.

        Returns:
            list[list[int]]: List of hydride bonds. [index of H, index of M]
        """

        # return variable
        hydride_bond_indices = []

        for i in range(len(qm_data.atomic_numbers)):

            # look for transition metals
            if qm_data.atomic_numbers[i] in ElementLookUpTable.transition_metal_atomic_numbers:
                # get bound atom indices and append to return variable
                hydride_hydrogen_indices = self._get_bound_h_atom_indices(i, qm_data, threshold=self.settings.hydrogen_count_threshold)

                for j in range(len(hydride_hydrogen_indices)):
                    hydride_bond_indices.append([hydride_hydrogen_indices[j], i])

        return hydride_bond_indices

    def _get_bound_atom_indices(self, atom_index: int, qm_data: QmData, threshold: float):

        """Gets the indices of bound atoms of a given atom.

        Returns:
            list[int]: List of h atom indices.
        """

        # check if given atom index is valid
        if atom_index < 0 or atom_index > qm_data.n_atoms - 1:
            raise ValueError('The specified node index is out of range. Valid range: 0 - ' +
                             str(qm_data.n_atoms - 1) + '. Given: ' + str(atom_index) + '.')

        # return variable
        bound_atom_indices = []

        # get appropriate index matrix
        index_matrix = self._get_index_matrix(qm_data)

        for i in range(len(index_matrix[atom_index])):

            # skip self interaction
            if i == atom_index:
                continue

            # check for bond index
            if index_matrix[atom_index][i] > threshold:
                bound_atom_indices.append(i)

        return bound_atom_indices

    def _get_bound_h_atom_indices(self, atom_index: int, qm_data: QmData, threshold: float = None):

        """Gets the indices of bound h atoms of a given atom.

        Returns:
            list[int]: List of h atom indices.
        """

        # resolve threshold
        if threshold is None:
            threshold = self.settings.hydrogen_count_threshold

        # return variable
        bound_h_indices = []

        # get all bound atom indices
        # use hydrogen threshold
        bound_atom_indices = self._get_bound_atom_indices(atom_index, qm_data, threshold=threshold)

        for i in range(len(bound_atom_indices)):

            # append if hydrogen
            if qm_data.atomic_numbers[bound_atom_indices[i]] == 1:
                bound_h_indices.append(bound_atom_indices[i])

        return bound_h_indices

    def _determine_hydrogen_count(self, atom_index: int, qm_data: QmData):

        """Determines how many hyrdogen atoms are bound to the atom with the specified index.

        Returns:
            int: The number of bound hydrogen atoms.
        """

        return len(self._get_bound_h_atom_indices(atom_index, qm_data))

    def _get_index_matrix(self, qm_data: QmData):

        """Helper function that returns the appropriate index matrix based on the GraphGenerator settings.

        Raises:
            ValueError: If a bond determination mode is selected that can not be resolved.

        Returns:
            list[list[float]]: The selected index matrix.
        """

        # decide which index matrix to return

        # Wiberg mode
        if self.settings.bond_determination_mode == BondDeterminationMode.WIBERG:
            return qm_data.wiberg_index_matrix
        # LMO mode
        elif self.settings.bond_determination_mode == BondDeterminationMode.LMO:
            return qm_data.lmo_bond_order_matrix
        # NLMO mode
        elif self.settings.bond_determination_mode == BondDeterminationMode.NLMO:
            return qm_data.nbo_bond_order_matrix
        # raise exception otherwise
        else:
            raise ValueError('Bond determination mode not recognised.')

    def _get_graph_features(self, qm_data: QmData) -> list:

        # return variable
        graph_feature_list = []

        for i in range(len(self.settings.graph_features)):

            if self.settings.graph_features[i] == GraphFeature.N_ATOMS:
                graph_feature_list.append(qm_data.n_atoms)
            elif self.settings.graph_features[i] == GraphFeature.MOLECULAR_MASS:
                graph_feature_list.append(qm_data.molecular_mass)
            elif self.settings.graph_features[i] == GraphFeature.POLARISABILITY:
                graph_feature_list.append(qm_data.polarisability)
            elif self.settings.graph_features[i] == GraphFeature.CHARGE:
                graph_feature_list.append(qm_data.charge)
            else:
                warnings.warn('Could not find target' + str(self.settings.graph_features[i]) + '.')

        return graph_feature_list

    def _get_targets(self, qm_data: QmData):

        """Helper function to resolve which targets to use.

        Returns:
            list[float]: List of graph targets.
        """

        # return variable
        target_list = []

        for i in range(len(self.settings.targets)):

            if type(self.settings.targets[i]) is not QmTarget:
                warnings.warn('Element ' + str(i) + ' of list is not of type QmTarget. Entry will be skipped.')

            if self.settings.targets[i] == QmTarget.SVP_ELECTRONIC_ENERGY:
                target_list.append(qm_data.svp_electronic_energy)
            elif self.settings.targets[i] == QmTarget.TZVP_ELECTRONIC_ENERGY:
                target_list.append(qm_data.tzvp_electronic_energy)
            elif self.settings.targets[i] == QmTarget.SVP_DISPERSION_ENERGY:
                target_list.append(qm_data.svp_dispersion_energy)
            elif self.settings.targets[i] == QmTarget.TZVP_DISPERSION_ENERGY:
                target_list.append(qm_data.tzvp_dispersion_energy)
            elif self.settings.targets[i] == QmTarget.SVP_DIPOLE_MOMENT:
                target_list.append(qm_data.svp_dipole_moment)
            elif self.settings.targets[i] == QmTarget.TZVP_DIPOLE_MOMENT:
                target_list.append(qm_data.tzvp_dipole_moment)
            elif self.settings.targets[i] == QmTarget.SVP_HOMO_ENERGY:
                target_list.append(qm_data.svp_homo_energy)
            elif self.settings.targets[i] == QmTarget.TZVP_HOMO_ENERGY:
                target_list.append(qm_data.tzvp_homo_energy)
            elif self.settings.targets[i] == QmTarget.SVP_LUMO_ENERGY:
                target_list.append(qm_data.svp_lumo_energy)
            elif self.settings.targets[i] == QmTarget.TZVP_LUMO_ENERGY:
                target_list.append(qm_data.tzvp_lumo_energy)
            elif self.settings.targets[i] == QmTarget.SVP_HOMO_LUMO_GAP:
                target_list.append(qm_data.svp_homo_lumo_gap)
            elif self.settings.targets[i] == QmTarget.TZVP_HOMO_LUMO_GAP:
                target_list.append(qm_data.tzvp_homo_lumo_gap)
            elif self.settings.targets[i] == QmTarget.LOWEST_VIBRATIONAL_FREQUENCY:
                target_list.append(qm_data.lowest_vibrational_frequency)
            elif self.settings.targets[i] == QmTarget.HIGHEST_VIBRATIONAL_FREQUENCY:
                target_list.append(qm_data.highest_vibrational_frequency)
            elif self.settings.targets[i] == QmTarget.HEAT_CAPACITY:
                target_list.append(qm_data.heat_capacity)
            elif self.settings.targets[i] == QmTarget.ENTROPY:
                target_list.append(qm_data.entropy)
            elif self.settings.targets[i] == QmTarget.ZPE_CORRECTION:
                target_list.append(qm_data.zpe_correction)
            elif self.settings.targets[i] == QmTarget.ENTHALPY_ENERGY:
                target_list.append(qm_data.enthalpy_energy)
            elif self.settings.targets[i] == QmTarget.GIBBS_ENERGY:
                target_list.append(qm_data.gibbs_energy)
            elif self.settings.targets[i] == QmTarget.CORRECTED_ENTHALPY_ENERGY:
                target_list.append(qm_data.corrected_enthalpy_energy)
            elif self.settings.targets[i] == QmTarget.CORRECTED_GIBBS_ENERGY:
                target_list.append(qm_data.corrected_gibbs_energy)
            elif self.settings.targets[i] == QmTarget.ELECTRONIC_ENERGY_DELTA:
                target_list.append(qm_data.electronic_energy_delta)
            elif self.settings.targets[i] == QmTarget.DISPERSION_ENERGY_DELTA:
                target_list.append(qm_data.dispersion_energy_delta)
            elif self.settings.targets[i] == QmTarget.DIPOLE_MOMENT_DELTA:
                target_list.append(qm_data.dipole_moment_delta)
            elif self.settings.targets[i] == QmTarget.HOMO_LUMO_GAP_DELTA:
                target_list.append(qm_data.homo_lumo_gap_delta)
            else:
                warnings.warn('Could not find target' + str(self.settings.targets[i]) + '.')

        return target_list

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
