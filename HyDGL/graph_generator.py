import warnings
from statistics import mean

from .enums.nbo_type import NboType
from .enums.edge_type import EdgeType
from .nbo_data_point import NboDataPoint
from .enums.sopa_edge_feature import SopaEdgeFeature

from .node import Node
from .edge import Edge
from .graph import Graph
from .qm_data import QmData
from .enums.qm_target import QmTarget
from .enums.edge_feature import EdgeFeature
from .enums.node_feature import NodeFeature
from .enums.hydrogen_mode import HydrogenMode
from .enums.graph_feature import GraphFeature
from .enums.bond_order_type import BondOrderType
from .element_look_up_table import ElementLookUpTable
from .enums.sopa_resolution_mode import SopaResolutionMode
from .graph_generator_settings import GraphGeneratorSettings


class GraphGenerator:

    """Class to generate appropriate graphs based on supplied QM data."""

    def __init__(self, settings: GraphGeneratorSettings):
        """Constructor

        Args:
            settings (GraphGeneratorSettings): Settings for GG.
        """

        self._settings = settings

    def generate_graph(self, qm_data: QmData) -> Graph:

        """Generates a graph according to the specified settings.

        Returns:
            Graph: The graph representation of the graph.
        """

        # get edges
        nodes = self._get_nodes(qm_data)

        # get edges
        edges = []
        if EdgeType.BOND_ORDER_METAL in self._settings.edge_types or \
           EdgeType.BOND_ORDER_NON_METAL in self._settings.edge_types or \
           EdgeType.NBO_BONDING_ORBITALS in self._settings.edge_types:
            edges += self._get_edges(qm_data)
        if EdgeType.SOPA in self._settings.edge_types:
            edges += self._get_sopa_edges(qm_data)

        # rescale node references in edges if explicit hydrogens were omitted
        if self._settings.hydrogen_mode == HydrogenMode.OMIT:
            edges = self._adjust_node_references(edges, qm_data)

        # add final node degree as node feature
        if NodeFeature.NODE_DEGREE in self._settings.node_features:

            node_degrees = [0 for _ in nodes]

            for edge in edges:
                for node_index in edge.node_indices:
                    node_degrees[node_index] += 1

            for i, node in enumerate(nodes):
                node.features['node_degree'] = node_degrees[i]

        # check validity of nodes
        self._validate_node_list(nodes)
        # check validity of edges
        self._validate_edge_list(edges, len(nodes))

        # get graph features
        graph_features = self._get_graph_features(qm_data)

        # get targets
        targets = self._get_targets(qm_data)

        # get meta_data
        meta_data = self._get_meta_data(qm_data)

        return Graph(nodes,
                     edges,
                     targets=targets,
                     graph_features=graph_features,
                     meta_data=meta_data)

    # deprecated
    def _get_node_labels(self, qm_data: QmData) -> list[str]:

        """Gets the labels for the nodes in terms of the element identifiers.

        Returns:
            list[string]: List of element identifiers.
        """

        node_indices = self._get_nodes_to_extract_indices(qm_data)
        return [ElementLookUpTable.get_element_identifier(qm_data.atomic_numbers[node_index]) for node_index in node_indices]

    # deprecated
    def _get_node_positions(self, qm_data: QmData) -> list[list[float]]:

        """Gets the 3d positions for the nodes in terms of the element identifiers.

        Returns:
            list[list[float]]: List of 3d positions.
        """

        node_indices = self._get_nodes_to_extract_indices(qm_data)
        return [(qm_data.geometric_data[node_index]) for node_index in node_indices]

    def _get_edges(self, qm_data: QmData) -> list[Edge]:

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

        return edges

    def _get_nbo_bonding_orbital_adjacency_list(self, qm_data: QmData) -> list[list[int]]:

        """Gets the NBO bond orbital adjacency list.

        Returns:
            list[list[int]]: The NBO bond orbital adjacency list.
        """

        # set up adjacency list
        adjacency_list = []

        # iterate through two-atom bonds
        for i in range(len(qm_data.bond_pair_data)):

            # ignore hydrogens in omit and implicit mode
            if self._settings.hydrogen_mode == HydrogenMode.OMIT:
                if qm_data.atomic_numbers[qm_data.bond_pair_data[i].atom_indices[0]] == 1 or \
                   qm_data.atomic_numbers[qm_data.bond_pair_data[i].atom_indices[1]] == 1:
                    continue

            # skip if bond length larger than max allowed
            if qm_data.bond_distance_matrix[qm_data.bond_pair_data[i].atom_indices[0]][qm_data.bond_pair_data[i].atom_indices[1]] > self._settings.max_bond_distance:
                continue


            if not qm_data.bond_pair_data[i].atom_indices in adjacency_list:
                adjacency_list.append(qm_data.bond_pair_data[i].atom_indices)

        # iterate through three-atom bonds
        for i in range(len(qm_data.bond_3c_data)):

            # ignore hydrogens in omit and implicit mode
            if self._settings.hydrogen_mode == HydrogenMode.OMIT:
                if qm_data.atomic_numbers[qm_data.bond_3c_data[i].atom_indices[0]] == 1 or \
                   qm_data.atomic_numbers[qm_data.bond_3c_data[i].atom_indices[1]] == 1 or \
                   qm_data.atomic_numbers[qm_data.bond_3c_data[i].atom_indices[2]] == 1:
                    continue

            # NOTE: For a 3c bond A-B-C This only connects A with B and B with C.
            # For some situations (e.g. in Boranes) this might not reflect the
            # relevant physics.
            if not qm_data.bond_3c_data[i].atom_indices[0:2] in adjacency_list:
                adjacency_list.append(qm_data.bond_3c_data[i].atom_indices[0:2])

            if not qm_data.bond_3c_data[i].atom_indices[1:3] in adjacency_list:
                adjacency_list.append(qm_data.bond_3c_data[i].atom_indices[1:3])

        return sorted(adjacency_list)

    def _get_bond_order_adjacency_list(self, qm_data: QmData) -> list[list[int]]:

        """Gets an adjacency list using bond orders of the specified type.

        Returns:
            list[list[int]]: The bond order adjacency list.
        """

        metal_adjacency_list = self._get_bond_order_metal_adjacency_list(qm_data)
        non_metal_adjacency_list = self._get_bond_order_non_metal_adjacency_list(qm_data)

        return metal_adjacency_list + non_metal_adjacency_list

    def _get_bond_order_non_metal_adjacency_list(self, qm_data: QmData) -> list[list[int]]:

        """Gets an adjacency list using bond orders of the specified type only for non-metal atoms.

        Returns:
            list[list[int]]: The bond order adjacency list for all non-metal atoms.
        """

        threshold = self._settings.bond_threshold

        adjacency_list = []

        # get appropriate index matrix
        index_matrix = self._get_index_matrix(qm_data, self._settings.bond_order_mode)

        # iterate over half triangle matrix to determine bonds
        for i in range(len(index_matrix) - 1):

            # skip if metal atom
            if qm_data.atomic_numbers[i] in ElementLookUpTable.transition_metal_atomic_numbers:
                continue

            for j in range(i + 1, len(index_matrix), 1):

                # skip if metal atom
                if qm_data.atomic_numbers[j] in ElementLookUpTable.transition_metal_atomic_numbers:
                    continue

                # skip if bond length larger than max allowed
                if qm_data.bond_distance_matrix[i][j] > self._settings.max_bond_distance:
                    continue

                # if larger than threshold --> add bond
                if (index_matrix[i][j]) > threshold:

                    # ignore hydrogens in omit and implicit mode
                    if self._settings.hydrogen_mode == HydrogenMode.OMIT:
                        if qm_data.atomic_numbers[i] == 1 or qm_data.atomic_numbers[j] == 1:
                            continue

                    # append atom pair
                    adjacency_list.append([i, j])

        return adjacency_list

    def _get_bond_order_metal_adjacency_list(self, qm_data: QmData) -> list[list[int]]:

        """Gets an adjacency list using bond orders of the specified type only for metal atoms.

        Returns:
            list[list[int]]: The bond order adjacency list for all metal atoms.
        """

        threshold = self._settings.bond_threshold_metal

        adjacency_list = []

        # get appropriate index matrix
        index_matrix = self._get_index_matrix(qm_data, self._settings.bond_order_mode)

        # iterate over half triangle matrix to determine bonds
        for i in range(len(index_matrix) - 1):

            for j in range(i + 1, len(index_matrix), 1):

                # skip if metal atom
                if qm_data.atomic_numbers[i] not in ElementLookUpTable.transition_metal_atomic_numbers and \
                   qm_data.atomic_numbers[j] not in ElementLookUpTable.transition_metal_atomic_numbers:
                    continue

                # skip if bond length larger than max allowed
                if qm_data.bond_distance_matrix[i][j] > self._settings.max_bond_distance:
                    continue

                # if larger than threshold --> add bond
                if (index_matrix[i][j]) > threshold:

                    # ignore hydrogens in omit and implicit mode
                    if self._settings.hydrogen_mode == HydrogenMode.OMIT:
                        if qm_data.atomic_numbers[i] == 1 or qm_data.atomic_numbers[j] == 1:
                            continue

                    # append atom pair
                    adjacency_list.append([i, j])

        return adjacency_list

    def _get_adjacency_list(self, qm_data: QmData) -> list[list[int]]:

        """Gets the adjacency list of the system according to edge settings.

        Returns:
            list[list[int]]: A list of atom index pairs for the edges.
        """

        adjacency_list = []

        if EdgeType.NBO_BONDING_ORBITALS in self._settings.edge_types:
            adjacency_list.extend(self._get_nbo_bonding_orbital_adjacency_list(qm_data))

        if EdgeType.BOND_ORDER_METAL in self._settings.edge_types:
            adjacency_list.extend(self._get_bond_order_metal_adjacency_list(qm_data))

        if EdgeType.BOND_ORDER_NON_METAL in self._settings.edge_types:
            adjacency_list.extend(self._get_bond_order_non_metal_adjacency_list(qm_data))

        # get hydride bonds and append if not already in list
        hydride_bonds = self._get_hydride_bond_indices(qm_data)
        for hydride_bond in hydride_bonds:

            if hydride_bond not in adjacency_list and list(reversed(hydride_bond)) not in adjacency_list:
                adjacency_list.append(hydride_bond)

        set_list = [list(item) for item in set(tuple(atom_indices) for atom_indices in adjacency_list)]
        return list(sorted(set_list))

    def _get_edge_features(self, bond_atom_indices: list[int], qm_data: QmData) -> list[float]:

        """Gets the edge features for given atom indices according to specification.

        Returns:
            list[float]: A list of edge features.
        """

        # pre read data for efficiency

        # bonds from BD
        bond_pair_atom_indices = [x.atom_indices for x in qm_data.bond_pair_data]
        # bonds from 3c
        # bond_3c_atom_indices = [x.atom_indices for x in qm_data.bond_3c_data]
        # gets the A-B and B-C bond pairs from 3c data
        bond_3c_atom_indices = [x.atom_indices[0:2] for x in qm_data.bond_3c_data] + [x.atom_indices[1:3] for x in qm_data.bond_3c_data]

        # setup edge_features
        edge_features = {}

        # append requested bond orders
        if EdgeFeature.WIBERG_BOND_ORDER in self._settings.edge_features:
            edge_features['wiberg_bond_order'] = qm_data.wiberg_bond_order_matrix[bond_atom_indices[0]][bond_atom_indices[1]]
        if EdgeFeature.LMO_BOND_ORDER in self._settings.edge_features:
            edge_features['lmo_bond_order'] = qm_data.lmo_bond_order_matrix[bond_atom_indices[0]][bond_atom_indices[1]]
        if EdgeFeature.NLMO_BOND_ORDER in self._settings.edge_features:
            edge_features['nlmo_bond_order'] = qm_data.nlmo_bond_order_matrix[bond_atom_indices[0]][bond_atom_indices[1]]

        # append requested integer bond orders
        if EdgeFeature.WIBERG_BOND_ORDER_INT in self._settings.edge_features:

            wiberg_index = qm_data.wiberg_bond_order_matrix[bond_atom_indices[0]][bond_atom_indices[1]]
            bond_order_int = 0

            if wiberg_index < 1.43:
                bond_order_int = 1
            elif wiberg_index >= 1.43 and wiberg_index < 2.0:
                bond_order_int = 2
            elif wiberg_index >= 2.0:
                bond_order_int = 3

            edge_features['wiberg_bond_order_int'] = bond_order_int

        # add bond distance as feature to edges
        if EdgeFeature.BOND_DISTANCE in self._settings.edge_features:
            edge_features['bond_distance'] = qm_data.bond_distance_matrix[bond_atom_indices[0]][bond_atom_indices[1]]

        if EdgeFeature.NBO_TYPE in self._settings.edge_features:

            if bond_atom_indices in bond_3c_atom_indices:
                edge_features['nbo_type'] = '3C'
            elif bond_atom_indices in bond_pair_atom_indices:
                edge_features['nbo_type'] = 'BD'
            else:
                edge_features['nbo_type'] = 'None'

        # add number of bond/antibond orbitals if requested
        if EdgeFeature.BOND_ORBITAL_MAX in self._settings.edge_features or \
                EdgeFeature.BOND_ORBITAL_AVERAGE in self._settings.edge_features or \
                EdgeFeature.BOND_ENERGY_MIN_MAX_DIFFERENCE in self._settings.edge_features:

            if bond_atom_indices in bond_3c_atom_indices:
                edge_features['n_bn'] = len([x.energy for x in qm_data.bond_3c_data if x.contains_atom_indices(bond_atom_indices)])
            elif bond_atom_indices in bond_pair_atom_indices:
                edge_features['n_bn'] = len([x.energy for x in qm_data.bond_pair_data if x.atom_indices == bond_atom_indices])
            else:
                edge_features['n_bn'] = 0

        # add number of bond/antibond orbitals if requested
        if EdgeFeature.ANTIBOND_ORBITAL_MIN in self._settings.edge_features or \
                EdgeFeature.ANTIBOND_ORBITAL_AVERAGE in self._settings.edge_features or \
                EdgeFeature.ANTIBOND_ENERGY_MIN_MAX_DIFFERENCE in self._settings.edge_features:

            if bond_atom_indices in bond_3c_atom_indices:
                edge_features['n_nbn'] = len([x.energy for x in qm_data.antibond_3c_data if x.contains_atom_indices(bond_atom_indices)]) + \
                                        len([x.energy for x in qm_data.nonbond_3c_data if x.contains_atom_indices(bond_atom_indices)])
            elif bond_atom_indices in bond_pair_atom_indices:
                edge_features['n_nbn'] = len([x.energy for x in qm_data.antibond_pair_data if x.atom_indices == bond_atom_indices])
            else:
                edge_features['n_nbn'] = 0

        if EdgeFeature.BOND_ENERGY_MIN_MAX_DIFFERENCE in self._settings.edge_features:

            if bond_atom_indices in bond_3c_atom_indices:
                energies = [x.energy for x in qm_data.bond_3c_data if x.contains_atom_indices(bond_atom_indices)]
            elif bond_atom_indices in bond_pair_atom_indices:
                energies = [x.energy for x in qm_data.bond_pair_data if x.atom_indices == bond_atom_indices]
            else:
                energies = []

            # append difference if there are 2 entries or more
            if len(energies) >= 2:
                edge_features['bond_energy_min_max_difference'] = abs(min(energies) - max(energies))
            # append 0 otherwise
            else:
                edge_features['bond_energy_min_max_difference'] = 0.0

        if EdgeFeature.BOND_ORBITAL_MAX in self._settings.edge_features and len(self._settings.bond_orbital_indices) >= 0:

            if bond_atom_indices in bond_3c_atom_indices:
                edge_features = edge_features | self._get_maximum_energy_nbo(qm_data, bond_atom_indices, NboType.THREE_CENTER_BOND)
            elif bond_atom_indices in bond_pair_atom_indices:
                edge_features = edge_features | self._get_maximum_energy_nbo(qm_data, bond_atom_indices, NboType.BOND)
            else:
                edge_features = edge_features | self._get_default_nbo(qm_data, NboType.BOND, feature_name='max')

        if EdgeFeature.BOND_ORBITAL_AVERAGE in self._settings.edge_features and len(self._settings.bond_orbital_indices) >= 0:

            if bond_atom_indices in bond_3c_atom_indices:
                edge_features = edge_features | self._get_average_nbo(qm_data, bond_atom_indices, NboType.THREE_CENTER_BOND)
            elif bond_atom_indices in bond_pair_atom_indices:
                edge_features = edge_features | self._get_average_nbo(qm_data, bond_atom_indices, NboType.BOND)
            else:
                edge_features = edge_features | self._get_default_nbo(qm_data, NboType.BOND, feature_name='average')

        if EdgeFeature.ANTIBOND_ENERGY_MIN_MAX_DIFFERENCE in self._settings.edge_features:

            if bond_atom_indices in bond_3c_atom_indices:
                energies = [x.energy for x in qm_data.antibond_3c_data if x.contains_atom_indices(bond_atom_indices)]
            elif bond_atom_indices in bond_pair_atom_indices:
                energies = [x.energy for x in qm_data.antibond_pair_data if x.atom_indices == bond_atom_indices]
            else:
                energies = []

            # append difference if there are 2 entries or more
            if len(energies) >= 2:
                edge_features['antibond_energy_min_max_difference'] = abs(min(energies) - max(energies))
            # append 0 otherwise
            else:
                edge_features['antibond_energy_min_max_difference'] = 0.0

        if EdgeFeature.ANTIBOND_ORBITAL_MIN in self._settings.edge_features and len(self._settings.antibond_orbital_indices) >= 0:

            if bond_atom_indices in bond_3c_atom_indices:
                edge_features = edge_features | self._get_minimum_energy_nbo(qm_data, bond_atom_indices, NboType.THREE_CENTER_ANTIBOND)
            elif bond_atom_indices in bond_pair_atom_indices:
                edge_features = edge_features | self._get_minimum_energy_nbo(qm_data, bond_atom_indices, NboType.ANTIBOND)
            else:
                edge_features = edge_features | self._get_default_nbo(qm_data, NboType.ANTIBOND, feature_name='min')

        if EdgeFeature.ANTIBOND_ORBITAL_AVERAGE in self._settings.edge_features and len(self._settings.antibond_orbital_indices) >= 0:

            if bond_atom_indices in bond_3c_atom_indices:
                edge_features = edge_features | self._get_average_nbo(qm_data, bond_atom_indices, NboType.THREE_CENTER_ANTIBOND)
            elif bond_atom_indices in bond_pair_atom_indices:
                edge_features = edge_features | self._get_average_nbo(qm_data, bond_atom_indices, NboType.ANTIBOND)
            else:
                edge_features = edge_features | self._get_default_nbo(qm_data, NboType.ANTIBOND, feature_name='average')

        return edge_features

    def _get_minimum_energy_nbo(self, qm_data: QmData, atom_indices: list, nbo_type: NboType) -> dict:

        """Gets a dict of the minimum energy NBO entry.

        Returns:
            dict: The NBO data dict.
        """

        return self._get_extremum_energy_nbo(qm_data, atom_indices, nbo_type, min)

    def _get_maximum_energy_nbo(self, qm_data: QmData, atom_indices: list, nbo_type: NboType) -> dict:

        """Gets a dict of the maximum energy NBO entry.

        Returns:
            dict: The NBO data dict.
        """

        return self._get_extremum_energy_nbo(qm_data, atom_indices, nbo_type, max)

    def _get_extremum_energy_nbo(self, qm_data: QmData, atom_indices: list, nbo_type: NboType, extremum_operator) -> dict:

        """Gets a dict of the extremum energy NBO entry.

        Returns:
            dict: The NBO data dict.
        """

        # resolve nbo type
        nbo_data = qm_data.get_nbo_data_by_type(nbo_type)
        nbo_orbital_indices = self._settings.get_nbo_orbital_indices_by_type(nbo_type)
        nbo_energies = [x.energy for x in nbo_data]

        # return variable
        nbo_features = {}
        # base name to setup dict
        base_name = str(nbo_type).split('.')[1].lower().replace('three_center_', '') + '_' + extremum_operator.__name__

        # energies
        energies = [x.energy for x in nbo_data if x.contains_atom_indices(atom_indices)]

        # select index of the extremum energy
        selected_index = nbo_energies.index(extremum_operator(energies))

        # append data (total length = 2 + number of orbital occupancies)
        nbo_features[base_name + '_energy'] = nbo_data[selected_index].energy
        nbo_features[base_name + '_occupation'] = nbo_data[selected_index].occupation

        # get values for orbital symmetries of energy extremum
        for k in nbo_orbital_indices:
            nbo_features[base_name + '_' + ['s', 'p','d', 'f'][k] + '_occupation'] = nbo_data[selected_index].orbital_occupations[k]

        return nbo_features

    def _get_average_nbo(self, qm_data: QmData, atom_indices: list, nbo_type: NboType) -> dict:

        """Gets a dict of the average NBO entry.

        Returns:
            dict: The NBO data dict.
        """

        # resolve nbo type
        nbo_data = qm_data.get_nbo_data_by_type(nbo_type)
        nbo_orbital_indices = self._settings.get_nbo_orbital_indices_by_type(nbo_type)

        # return variable
        nbo_features = {}
        # base name to setup dict
        base_name = str(nbo_type).split('.')[1].lower().replace('three_center_', '') + '_average'

        # get list of all energies of this NBO
        energies = [x.energy for x in nbo_data if x.contains_atom_indices(atom_indices)]
        # get list of all occupation values for this NBO
        occupations = [x.occupation for x in nbo_data if x.contains_atom_indices(atom_indices)]
        # get list of symmetry values of different lone pairs for this NBO
        symmetries = [x.orbital_occupations for x in nbo_data if x.contains_atom_indices(atom_indices)]

        # append data (total length = 2 + number of orbital occupancies)
        nbo_features[base_name + '_energy'] = mean(energies)
        nbo_features[base_name + '_occupation'] = mean(occupations)

        # get values for orbital symmetries of energy extremum
        for k in nbo_orbital_indices:
            nbo_features[base_name + '_' + ['s', 'p','d', 'f'][k] + '_occupation'] = mean([x[k] for x in symmetries])

        return nbo_features

    def _get_default_nbo(self, qm_data: QmData, nbo_type: NboType, feature_name: str = 'default') -> dict:

        """Gets a dict of the default NBO entry.

        Returns:
            dict: The NBO data dict.
        """

        # resolve nbo type
        nbo_orbital_indices = self._settings.get_nbo_orbital_indices_by_type(nbo_type)

        # return variable
        nbo_features = {}
        # base name to setup dict
        base_name = str(nbo_type).split('.')[1].lower().replace('three_center_', '') + '_' + feature_name

        nbo_features[base_name + '_energy'] = 0.0
        nbo_features[base_name + '_occupation'] = 0.0

        symmetries = self._get_default_orbital_occupations(qm_data, nbo_type)

        # get values for orbital symmetries of energy extremum
        for k in nbo_orbital_indices:
            nbo_features[base_name + '_' + ['s', 'p','d', 'f'][k] + '_occupation'] = symmetries[k]

        return nbo_features

    def _get_default_orbital_occupations(self, qm_data: QmData, nbo_type: NboType):

        """Returns the default values for occupations used when no NBO data for a specific edge is available. The orbital
           occupancies are used as specified in the settings.

        Returns:
            list[float]: The default orbital occupations.
        """

        if nbo_type == NboType.BOND or nbo_type == NboType.THREE_CENTER_BOND:
            average_occupations = self._get_average_orbital_occupations(qm_data.bond_pair_data)
            return [average_occupations[i] for i in self._settings.bond_orbital_indices]
        elif nbo_type == NboType.ANTIBOND or nbo_type == NboType.THREE_CENTER_ANTIBOND or nbo_type == NboType.THREE_CENTER_NONBOND:
            average_occupations = self._get_average_orbital_occupations(qm_data.antibond_pair_data)
            return [average_occupations[i] for i in self._settings.antibond_orbital_indices]
        elif nbo_type == NboType.LONE_PAIR:
            return len(self._settings.lone_pair_orbital_indices) * [0.0]
        elif nbo_type == NboType.LONE_VACANCY:
            return len(self._settings.lone_vacancy_orbital_indices) * [0.0]

    def _get_average_orbital_occupations(self, nbo_data: list[NboDataPoint]):

        """Gets average orbital occupancy of a list of NBO data points.

        Returns:
            list[float]: The averaged orbital occupancies ordered as [s, p, d, f].
        """

        orbital_occupations = [nbo_data[i].orbital_occupations for i in range(len(nbo_data))]
        average_orbital_occupations = list(map(mean, zip(*orbital_occupations)))
        return average_orbital_occupations

    def _get_featurised_edge(self, bond_atom_indices: list[int], qm_data: QmData) -> Edge:

        """Gets an edge object containing the edge indices as well as the request edge features.

        Returns:
            Edge: The edge object.
        """

        # get edge features
        edge_features = self._get_edge_features(bond_atom_indices, qm_data)

        # check if NBO edge or not and assign label/id
        if bond_atom_indices in [x.atom_indices for x in qm_data.bond_pair_data] or \
            bond_atom_indices in [x.atom_indices[0:2] for x in qm_data.bond_3c_data] + [x.atom_indices[1:3] for x in qm_data.bond_3c_data]:
            edge_label = 'NBO'
            edge_id = 'nbo-'
        else: 
            edge_label = 'BO'
            edge_id = 'bo-'

        return Edge(bond_atom_indices, features=edge_features, label=edge_label, id=edge_id)

    def _get_nodes(self, qm_data: QmData, include_misc_data: bool = True) -> list[Node]:

        """Gets a list of feature vectors for all nodes.

        Returns:
            list[list[floats]]: List of feature vectors of nodes.
        """

        node_indices = self._get_nodes_to_extract_indices(qm_data)

        nodes = []
        for i in range(len(node_indices)):

            nodes.append(self._get_individual_node(qm_data, node_indices[i], include_misc_data=include_misc_data))

        return nodes

    def _get_nodes_to_extract_indices(self, qm_data: QmData) -> list[int]:

        """Gets the list of node indices to be extracted depending on the used hydrogen mode.

        Returns:
            list[int]: List of node indices to extract.
        """

        node_indices = []
        for i in range(qm_data.n_atoms):

            # skip if hydrogen mode is not explicit
            if self._settings.hydrogen_mode == HydrogenMode.OMIT:
                if qm_data.atomic_numbers[i] == 1:
                    continue

            node_indices.append(i)

        # operations only relevant when not modelling hydrogens explicitly
        if self._settings.hydrogen_mode == HydrogenMode.OMIT:

            # check for hydride hydrogens to add explicitly
            hydride_bond_indices = self._get_hydride_bond_indices(qm_data)
            for i in range(len(hydride_bond_indices)):
                node_indices.append(hydride_bond_indices[i][0])

        # sort list before returning so that the order is correct
        return sorted(node_indices)

    def _get_individual_node(self, qm_data: QmData, atom_index: int, include_misc_data: bool = True) -> Node:

        """Gets the feature vector for one node.

        Returns:
            list[float]: The feature vector of the corresponding atom.
        """

        # for brevity
        i = atom_index

        # pre read data for efficiency

        # atom indices that have LP or LV
        lone_pair_atom_indices = [x.atom_indices[0] for x in qm_data.lone_pair_data]
        lone_vacancy_atom_indices = [x.atom_indices[0] for x in qm_data.lone_vacancy_data]

        # set up features for node
        node_features = {}

        # add basic features
        if NodeFeature.ATOMIC_NUMBER in self._settings.node_features:
            node_features['atomic_number'] = qm_data.atomic_numbers[i]
        if NodeFeature.COVALENT_RADIUS in self._settings.node_features:
            node_features['covalent_radius'] = ElementLookUpTable.atom_property_dict[ElementLookUpTable.get_element_identifier(qm_data.atomic_numbers[i])]['covalent_radius']
        if NodeFeature.ELECTRONEGATIVITY in self._settings.node_features:
            node_features['electronegativity'] = ElementLookUpTable.atom_property_dict[ElementLookUpTable.get_element_identifier(qm_data.atomic_numbers[i])]['electronegativity']

        # add natural atomic charge
        if NodeFeature.NATURAL_ATOMIC_CHARGE in self._settings.node_features:
            node_features['natural_atomic_charge'] = qm_data.natural_atomic_charges[i]

        # add natural electron populations
        if NodeFeature.NATURAL_ELECTRON_POPULATION_CORE in self._settings.node_features:
            node_features['natural_electron_population_core'] = qm_data.natural_electron_population[i][0]

        if NodeFeature.NATURAL_ELECTRON_POPULATION_VALENCE in self._settings.node_features:
            node_features['natural_electron_population_valence'] = qm_data.natural_electron_population[i][1]

        if NodeFeature.NATURAL_ELECTRON_POPULATION_RYDBERG in self._settings.node_features:
            node_features['natural_electron_population_rydberg'] = qm_data.natural_electron_population[i][2]

        if NodeFeature.NATURAL_ELECTRON_POPULATION_TOTAL in self._settings.node_features:
            node_features['natural_electron_population_total'] = sum(qm_data.natural_electron_population[i])

        # add natural electron configuration (requested orbital occupancies)
        for k in self._settings.natural_orbital_configuration_indices:
            node_features['natural_electron_configuration_' + ['s', 'p','d', 'f'][k] + '_occupation'] = qm_data.natural_electron_configuration[i][k]

        # add bond order totals

        # Wiberg mode
        if NodeFeature.WIBERG_BOND_ORDER_TOTAL in self._settings.node_features:
            node_features['wiberg_bond_order_total'] = qm_data.wiberg_bond_order_totals[i]
        # LMO mode
        if NodeFeature.LMO_BOND_ORDER_TOTAL in self._settings.node_features:
            node_features['lmo_bond_order_total'] = qm_data.lmo_bond_order_totals[i]
        # NLMO mode
        if NodeFeature.NLMO_BOND_ORDER_TOTAL in self._settings.node_features:
            node_features['nlmo_bond_order_total'] = qm_data.nlmo_bond_order_totals[i]

        # add number of lone pairs if requested
        if NodeFeature.LONE_PAIR_MAX in self._settings.node_features or \
                NodeFeature.LONE_PAIR_AVERAGE in self._settings.node_features or \
                NodeFeature.LONE_PAIR_ENERGY_MIN_MAX_DIFFERENCE in self._settings.node_features:

            node_features['n_lone_pairs'] = len([x.energy for x in qm_data.lone_pair_data if x.atom_indices[0] == i])

        if NodeFeature.LONE_PAIR_ENERGY_MIN_MAX_DIFFERENCE in self._settings.node_features:
            energies = [x.energy for x in qm_data.lone_pair_data if x.atom_indices[0] == i]

            # append difference if there are 2 entries or more
            if len(energies) >= 2:
                node_features['lone_pair_energy_min_max_difference'] = abs(min(energies) - max(energies))
            # append 0 otherwise
            else:
                node_features['lone_pair_energy_min_max_difference'] = 0.0

        if NodeFeature.LONE_PAIR_MAX in self._settings.node_features and len(self._settings.lone_pair_orbital_indices) >= 0:
            if i in lone_pair_atom_indices:
                node_features = node_features | self._get_maximum_energy_nbo(qm_data, [i], NboType.LONE_PAIR)
            else:
                node_features = node_features | self._get_default_nbo(qm_data, NboType.LONE_PAIR, feature_name='max')

        if NodeFeature.LONE_PAIR_AVERAGE in self._settings.node_features and len(self._settings.lone_pair_orbital_indices) >= 0:
            if i in lone_pair_atom_indices:
                node_features = node_features | self._get_average_nbo(qm_data, [i], NboType.LONE_PAIR)
            else:
                node_features = node_features | self._get_default_nbo(qm_data, NboType.LONE_PAIR, feature_name='average')

        # add number of lone vacancies if requested
        if NodeFeature.LONE_VACANCY_MIN in self._settings.node_features or \
                NodeFeature.LONE_VACANCY_AVERAGE in self._settings.node_features or \
                NodeFeature.LONE_VACANCY_ENERGY_MIN_MAX_DIFFERENCE in self._settings.node_features:

            node_features['n_lone_vacancies'] = len([x.energy for x in qm_data.lone_vacancy_data if x.atom_indices[0] == i])

        if NodeFeature.LONE_VACANCY_ENERGY_MIN_MAX_DIFFERENCE in self._settings.node_features:
            energies = [x.energy for x in qm_data.lone_vacancy_data if x.atom_indices[0] == i]

            # append difference if there are 2 entries or more
            if len(energies) >= 2:
                node_features['lone_vacancy_energy_min_max_difference'] = abs(min(energies) - max(energies))
            # append 0 otherwise
            else:
                node_features['lone_vacancy_energy_min_max_difference'] = 0.0

        if NodeFeature.LONE_VACANCY_MIN in self._settings.node_features and len(self._settings.lone_vacancy_orbital_indices) >= 0:
            if i in lone_vacancy_atom_indices:
                node_features = node_features | self._get_minimum_energy_nbo(qm_data, [i], NboType.LONE_VACANCY)
            else:
                node_features = node_features | self._get_default_nbo(qm_data, NboType.LONE_VACANCY, feature_name='min')

        if NodeFeature.LONE_VACANCY_AVERAGE in self._settings.node_features and len(self._settings.lone_vacancy_orbital_indices) >= 0:
            if i in lone_vacancy_atom_indices:
                node_features = node_features | self._get_average_nbo(qm_data, [i], NboType.LONE_VACANCY)
            else:
                node_features = node_features | self._get_default_nbo(qm_data, NboType.LONE_VACANCY, feature_name='average')

        # add implicit hydrogens
        if NodeFeature.BOUND_HYDROGEN_COUNT in self._settings.node_features:
            # get hydrogen count for heavy atoms in implicit mode
            hydrogen_count = None

            # set hydrogen count of hydrogens to 0
            if qm_data.atomic_numbers[i] == 1:
                hydrogen_count = 0
            # set hydrogen count to 0 if transition metal (will be modelled explicitly)
            elif qm_data.atomic_numbers[i] in ElementLookUpTable.transition_metal_atomic_numbers:
                hydrogen_count = 0
            # otherwise determine hydrogen count normally
            else:
                hydrogen_count = self._determine_hydrogen_count(i, qm_data)

            node_features['hydrogen_count'] = hydrogen_count

        if include_misc_data:

            # get node id, label and position
            node_id = 'node-' + str(i)
            node_label = ElementLookUpTable.get_element_identifier(qm_data.atomic_numbers[i])
            node_position = qm_data.geometric_data[i]

            return Node(features=node_features, position=node_position, label=node_label, id=node_id)
        return Node(features=node_features)

    def _adjust_node_references(self, edges: list[Edge], qm_data: QmData):

        """Rescales the node references for implicit/omit mode where hydrogens are not explicit nodes (except hydride hydrogens).

        Returns:
            list[list[int], list[float]]: Edges list with rescaled node references.
        """

        # get list of indices in use
        bond_atom_indices = list(set([item for sublist in [x.node_indices for x in edges] for item in sublist]))
        bond_atom_indices.sort()
        # loop through edges and replace node references
        for i in range(len(edges)):
            edges[i].node_indices[0] = edges[i].node_indices[0] - self._determine_hydrogen_position_offset(edges[i].node_indices[0], qm_data)
            edges[i].node_indices[1] = edges[i].node_indices[1] - self._determine_hydrogen_position_offset(edges[i].node_indices[1], qm_data)

        return edges

    def _determine_hydrogen_position_offset(self, atom_index: int, qm_data: QmData) -> int:

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

    def _get_hydride_hydrogen_indices(self, qm_data: QmData) -> list[int]:

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
                hydride_hydrogen_indices.extend(self._get_bound_h_atom_indices(i, qm_data, threshold=self._settings.hydrogen_count_threshold))

        return hydride_hydrogen_indices

    def _get_hydride_bond_indices(self, qm_data: QmData) -> list[list[int]]:

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
                hydride_hydrogen_indices = self._get_bound_h_atom_indices(i, qm_data, threshold=self._settings.hydrogen_count_threshold)

                for j in range(len(hydride_hydrogen_indices)):
                    hydride_bond_indices.append([hydride_hydrogen_indices[j], i])

        return hydride_bond_indices

    def _get_bound_atom_indices(self, atom_index: int, qm_data: QmData, threshold: float) -> list[int]:

        """Gets the indices of bound atoms of a given atom.

        Returns:
            list[int]: List of h atom indices.
        """

        # check if given atom index is valid
        if atom_index < 0 or atom_index > qm_data.n_atoms - 1:
            raise ValueError('The specified node index is out of range. Valid range: 0 - ' + str(qm_data.n_atoms - 1) + '. Given: ' + str(atom_index) + '.')

        # return variable
        bound_atom_indices = []

        # get appropriate index matrix
        index_matrix = self._get_index_matrix(qm_data, self._settings.bond_order_mode)

        for i in range(len(index_matrix[atom_index])):

            # skip self interaction
            if i == atom_index:
                continue

            # check for bond index
            if index_matrix[atom_index][i] > threshold:
                bound_atom_indices.append(i)

        return bound_atom_indices

    def _get_bound_h_atom_indices(self, atom_index: int, qm_data: QmData, threshold: float = None) -> list[int]:

        """Gets the indices of bound h atoms of a given atom.

        Returns:
            list[int]: List of h atom indices.
        """

        # resolve threshold
        if threshold is None:
            threshold = self._settings.hydrogen_count_threshold

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

    def _determine_hydrogen_count(self, atom_index: int, qm_data: QmData) -> int:

        """Determines how many hyrdogen atoms are bound to the atom with the specified index.

        Returns:
            int: The number of bound hydrogen atoms.
        """

        return len(self._get_bound_h_atom_indices(atom_index, qm_data))

    def _get_index_matrix(self, qm_data: QmData, bond_order_type: BondOrderType) -> list[list[float]]:

        """Helper function that returns the appropriate index matrix based on the GraphGenerator settings.

        Raises:
            ValueError: If a bond determination mode is selected that can not be resolved.

        Returns:
            list[list[float]]: The selected index matrix.
        """

        # decide which index matrix to return

        # Wiberg mode
        if bond_order_type == BondOrderType.WIBERG:
            return qm_data.wiberg_bond_order_matrix
        # LMO mode
        elif bond_order_type == BondOrderType.LMO:
            return qm_data.lmo_bond_order_matrix
        # NLMO mode
        elif bond_order_type == BondOrderType.NLMO:
            return qm_data.nlmo_bond_order_matrix
        # raise exception otherwise
        else:
            print('Bond determination mode not recognised. Defaulting to Wiberg')
            return qm_data.wiberg_bond_order_matrix

    def _get_graph_features(self, qm_data: QmData) -> dict:

        """Function to return the requested graph features.

        Returns:
            list[float]: A list of requested graph features.
        """

        # return variable
        graph_feature_dict = {}

        for i in range(len(self._settings.graph_features)):

            if self._settings.graph_features[i] == GraphFeature.N_ATOMS:
                graph_feature_dict['n_atoms'] = qm_data.n_atoms
            elif self._settings.graph_features[i] == GraphFeature.N_ELECTRONS:
                graph_feature_dict['n_electrons'] = sum(qm_data.atomic_numbers) - qm_data.charge
            elif self._settings.graph_features[i] == GraphFeature.MOLECULAR_MASS:
                graph_feature_dict['molecular_mass'] = qm_data.molecular_mass
            elif self._settings.graph_features[i] == GraphFeature.CHARGE:
                graph_feature_dict['charge'] = qm_data.charge
            else:
                warnings.warn('Could not find target' + str(self._settings.graph_features[i]) + '.')

        return graph_feature_dict

    def _get_targets(self, qm_data: QmData) -> list[float]:

        """Helper function to resolve which targets to use.

        Returns:
            list[float]: List of graph targets.
        """

        # return variable
        target_dict = {}

        for i in range(len(self._settings.targets)):

            if type(self._settings.targets[i]) is not QmTarget:
                warnings.warn('Element ' + str(i) + ' of list is not of type QmTarget. Entry will be skipped.')

            if self._settings.targets[i] == QmTarget.SVP_ELECTRONIC_ENERGY:
                target_dict['svp_electronic_energy'] = qm_data.svp_electronic_energy
            elif self._settings.targets[i] == QmTarget.TZVP_ELECTRONIC_ENERGY:
                target_dict['tzvp_electronic_energy'] = qm_data.tzvp_electronic_energy
            elif self._settings.targets[i] == QmTarget.SVP_DISPERSION_ENERGY:
                target_dict['svp_dispersion_energy'] = qm_data.svp_dispersion_energy
            elif self._settings.targets[i] == QmTarget.TZVP_DISPERSION_ENERGY:
                target_dict['tzvp_dispersion_energy'] = qm_data.tzvp_dispersion_energy
            elif self._settings.targets[i] == QmTarget.SVP_DIPOLE_MOMENT:
                target_dict['svp_dipole_moment'] = qm_data.svp_dipole_moment
            elif self._settings.targets[i] == QmTarget.TZVP_DIPOLE_MOMENT:
                target_dict['tzvp_dipole_moment'] = qm_data.tzvp_dipole_moment
            elif self._settings.targets[i] == QmTarget.SVP_HOMO_ENERGY:
                target_dict['svp_homo_energy'] = qm_data.svp_homo_energy
            elif self._settings.targets[i] == QmTarget.TZVP_HOMO_ENERGY:
                target_dict['tzvp_homo_energy'] = qm_data.tzvp_homo_energy
            elif self._settings.targets[i] == QmTarget.SVP_LUMO_ENERGY:
                target_dict['svp_lumo_energy'] = qm_data.svp_lumo_energy
            elif self._settings.targets[i] == QmTarget.TZVP_LUMO_ENERGY:
                target_dict['tzvp_lumo_energy'] = qm_data.tzvp_lumo_energy
            elif self._settings.targets[i] == QmTarget.SVP_HOMO_LUMO_GAP:
                target_dict['svp_homo_lumo_gap'] = qm_data.svp_homo_lumo_gap
            elif self._settings.targets[i] == QmTarget.TZVP_HOMO_LUMO_GAP:
                target_dict['tzvp_homo_lumo_gap'] = qm_data.tzvp_homo_lumo_gap
            elif self._settings.targets[i] == QmTarget.LOWEST_VIBRATIONAL_FREQUENCY:
                target_dict['lowest_vibrational_frequency'] = qm_data.lowest_vibrational_frequency
            elif self._settings.targets[i] == QmTarget.HIGHEST_VIBRATIONAL_FREQUENCY:
                target_dict['highest_vibrational_frequency'] = qm_data.highest_vibrational_frequency
            elif self._settings.targets[i] == QmTarget.HEAT_CAPACITY:
                target_dict['heat_capacity'] = qm_data.heat_capacity
            elif self._settings.targets[i] == QmTarget.ENTROPY:
                target_dict['entropy'] = qm_data.entropy
            elif self._settings.targets[i] == QmTarget.ZPE_CORRECTION:
                target_dict['zpe_correction'] = qm_data.zpe_correction
            elif self._settings.targets[i] == QmTarget.ENTHALPY_ENERGY:
                target_dict['enthalpy_energy'] = qm_data.enthalpy_energy
            elif self._settings.targets[i] == QmTarget.GIBBS_ENERGY:
                target_dict['gibbs_energy'] = qm_data.gibbs_energy
            elif self._settings.targets[i] == QmTarget.ENTHALPY_ENERGY_CORRECTION:
                target_dict['enthalpy_energy_correction'] = qm_data.enthalpy_energy_correction
            elif self._settings.targets[i] == QmTarget.GIBBS_ENERGY_CORRECTION:
                target_dict['gibbs_energy_correction'] = qm_data.gibbs_energy_correction
            elif self._settings.targets[i] == QmTarget.ELECTRONIC_ENERGY_DELTA:
                target_dict['electronic_energy_delta'] = qm_data.electronic_energy_delta
            elif self._settings.targets[i] == QmTarget.DISPERSION_ENERGY_DELTA:
                target_dict['dispersion_energy_delta'] = qm_data.dispersion_energy_delta
            elif self._settings.targets[i] == QmTarget.DIPOLE_MOMENT_DELTA:
                target_dict['dipole_moment_delta'] = qm_data.dipole_moment_delta
            elif self._settings.targets[i] == QmTarget.HOMO_LUMO_GAP_DELTA:
                target_dict['homo_lumo_gap_delta'] = qm_data.homo_lumo_gap_delta
            elif self._settings.targets[i] == QmTarget.POLARISABILITY:
                target_dict['polarisability'] = qm_data.polarisability
            elif self._settings.targets[i] == QmTarget.NORMALISED_POLARISABILITY:
                target_dict['normalised_polarisability'] = qm_data.polarisability / (sum(qm_data.atomic_numbers) - qm_data.charge)
            else:
                warnings.warn('Could not find target' + str(self._settings.targets[i]) + '.')

        return target_dict

    def _validate_node_list(self, nodes: list[Node]):

        """Checks the list of nodes for validity."""

        # check that all node vectors have the same length
        for i in range(1, len(nodes), 1):
            assert len(nodes[i].features) == len(nodes[0].features)

    def _validate_edge_list(self, edges: list[Edge], n_nodes: int):

        """Checks the list of edges for validity."""

        for i in range(0, len(edges), 1):

            # check that all edges are defined by two atom indices
            assert len(edges[i].node_indices) == 2
            # check that the edge defining atom indices are different
            # assert edges[i].node_indices[0] != edges[i].node_indices[1]
            # check that all edges have feature vectors of the same length
            assert len(edges[0].features) == len(edges[i].features)
            # check that the edge index identifiers are within the range of the number of atoms
            assert edges[i].node_indices[0] < n_nodes
            assert edges[i].node_indices[1] < n_nodes

    def _contains_hydrogen(self, qm_data: QmData, atom_indices: list[int]) -> bool:

        """Helper function to determine whether a given list of atom indices includes a hydrogen.

        Returns:
            bool: Boolean to indicate whether the list contains a hydrogen.
        """

        for atom_index in atom_indices:
            if self._is_hydrogen(qm_data, atom_index):
                return True
        return False

    def _contains_metal(self, qm_data: QmData, atom_indices: list[int]) -> bool:

        """Helper function to determine whether a given list of atom indices includes a metal.

        Returns:
            bool: Boolean to indicate whether the list contains a metal.
        """

        for atom_index in atom_indices:
            if self._is_metal(qm_data, atom_index):
                return True
        return False

    def _is_hydrogen_bond(self, qm_data: QmData, bond_atom_indices: list[int]) -> bool:

        """Helper function to determine whether a given bond includes a hydrogen.

        Raises:
            ValueError: If the list of bond atom indices is not equal to 2.

        Returns:
            bool: Boolean to indicate whether it is a hydrogen bond.
        """

        if len(bond_atom_indices) != 2:
            raise ValueError('The given list does not have length 2.')

        for atom_index in bond_atom_indices:
            if self._is_hydrogen(qm_data, atom_index):
                return True
        return False

    def _is_metal_bond(self, qm_data: QmData, bond_atom_indices: list[int]) -> bool:

        """Helper function to determine whether a given bond includes a transition metal.

        Raises:
            ValueError: If the list of bond atom indices is not equal to 2.

        Returns:
            bool: Boolean to indicate whether it is a transition metal bond.
        """

        if len(bond_atom_indices) != 2:
            raise ValueError('The given list does not have length 2.')

        for atom_index in bond_atom_indices:
            if self._is_metal(qm_data, atom_index):
                return True
        return False

    def _is_metal(self, qm_data: QmData, atom_index: int) -> bool:

        """Helper function to determine whether a given atom is a transition metal.

        Returns:
            bool: Boolean to indicate whether it is a transition metal.
        """

        if qm_data.atomic_numbers[atom_index] in ElementLookUpTable.transition_metal_atomic_numbers:
            return True
        return False

    def _is_hydrogen(self, qm_data: QmData, atom_index: int) -> bool:

        """Helper function to determine whether a given atom is a hydrogen.

        Returns:
            bool: Boolean to indicate whether it is a hydrogen.
        """

        if qm_data.atomic_numbers[atom_index] == 1:
            return True
        return False

    def _get_atom_indices_from_nbo_id(self, qm_data: QmData, nbo_id: int) -> list[int]:

        """Gets all atom indices associated to a NBO ID.

        Returns:
            list[int]: A list of atom indices.
        """

        nbo_list_index = next((i for i, item in enumerate(qm_data.nbo_data) if item.nbo_id == nbo_id), -1)
        return qm_data.nbo_data[nbo_list_index].atom_indices

    def _contribution_select_atom_indices_from_nbo_id(self, qm_data: QmData, nbo_id: int) -> list[int]:

        """Selects atom indices associated to a NBO ID based on their respective contributions.

        Returns:
            list[int]: A list of selected atom indices.
        """

        nbo_list_index = next((i for i, item in enumerate(qm_data.nbo_data) if item.nbo_id == nbo_id), -1)
        selected_atom_indices = []
        for i in range(len(qm_data.nbo_data[nbo_list_index].atom_indices)):
            if qm_data.nbo_data[nbo_list_index].contributions[i] >= self._settings.sopa_contribution_threshold:
                selected_atom_indices.append(qm_data.nbo_data[nbo_list_index].atom_indices[i])
        return selected_atom_indices

    def _get_nbo_type_from_nbo_id(self, qm_data: QmData, nbo_id: int) -> str:

        """Gets the type of NBO entry from NBO ID.

        Returns:
            str: A string indicating the NBO type.
        """

        nbo_list_index = next((i for i, item in enumerate(qm_data.nbo_data) if item.nbo_id == nbo_id), -1)
        if nbo_list_index == -1:
            raise ValueError()
        return qm_data.nbo_data[nbo_list_index].nbo_type

    def _get_nbo_from_nbo_id(self, qm_data: QmData, nbo_id: int) -> NboDataPoint:

        """Gets the data of a NBO from an ID.

        Returns:
            NboDataPoint: The NBO data.
        """

        for nbo_data_point in qm_data.nbo_data:
            if nbo_data_point.nbo_id == nbo_id:
                return nbo_data_point

        return None

    def _get_sopa_adjacency_list(self, qm_data: QmData) -> list[list[int]]:

        """Gets an adjacency list based on SOPA data. Also returns list of associated stabilisation energies and NBO types.

        Returns:
            list[list[int]]: Adjacency list.
            list[list[floats]]: Corresponding lists of associated stabilisation energies.
            list[list[str]]: Corresponding lists of asscociated NBO types.
        """

        # get list of hydride hydrogen indices
        hydride_hydrogen_indices = self._get_hydride_hydrogen_indices(qm_data)

        adjacency_list = []
        stabilisation_energies = []
        nbo_types = []
        nbo_ids = []
        for i in range(len(qm_data.sopa_data)):

            # skip if nbo type is not one of: LP, LV, BD, BD*
            if next((j for j, item in enumerate(qm_data.nbo_data) if item.nbo_id == qm_data.sopa_data[i][0][0]), -1) == -1:
                continue
            if next((j for j, item in enumerate(qm_data.nbo_data) if item.nbo_id == qm_data.sopa_data[i][0][1]), -1) == -1:
                continue

            # get all atom indices involved in the two nbo entries
            donor_atom_indices = self._get_atom_indices_from_nbo_id(qm_data, qm_data.sopa_data[i][0][0])
            acceptor_atom_indices = self._get_atom_indices_from_nbo_id(qm_data, qm_data.sopa_data[i][0][1])

            # in OMIT mode skip if it is a hydrogen interaction unless a metal is involved
            # this will skip any SOPA interaction that contains an hydrogen atom
            if self._settings.hydrogen_mode == HydrogenMode.OMIT:
                skip_sopa_entry = False
                atom_indices_collection = donor_atom_indices + acceptor_atom_indices
                # if self._contains_hydrogen(qm_data, atom_indices_collection) and not self._contains_metal(qm_data, atom_indices_collection):
                if self._contains_hydrogen(qm_data, atom_indices_collection):
                    # get hydrogen indices
                    atom_indices_collection_hydrogen_indices = [idx for idx in atom_indices_collection if qm_data.atomic_numbers[idx] == 1]
                    for hydrogen_index in atom_indices_collection_hydrogen_indices:
                        if hydrogen_index not in hydride_hydrogen_indices:
                            skip_sopa_entry = True

                if skip_sopa_entry:
                    continue

            donor_nbo_type = self._get_nbo_type_from_nbo_id(qm_data, qm_data.sopa_data[i][0][0])
            acceptor_nbo_type = self._get_nbo_type_from_nbo_id(qm_data, qm_data.sopa_data[i][0][1])

            # get selected atom indices involved in two nbo entries
            donor_selected_atom_indices = self._contribution_select_atom_indices_from_nbo_id(qm_data, qm_data.sopa_data[i][0][0])
            acceptor_selected_atom_indices = self._contribution_select_atom_indices_from_nbo_id(qm_data, qm_data.sopa_data[i][0][1])

            # add bond indices for each combination of indeces
            for index_a in donor_selected_atom_indices:
                for index_b in acceptor_selected_atom_indices:

                    selected_atom_indices = [index_a, index_b]

                    # add selected atom indices if not already in list
                    if selected_atom_indices not in adjacency_list:
                        adjacency_list.append(selected_atom_indices)
                        stabilisation_energies.append([qm_data.sopa_data[i][1][0]])
                        nbo_types.append([donor_nbo_type, acceptor_nbo_type])
                        nbo_ids.append([[qm_data.sopa_data[i][0][0], qm_data.sopa_data[i][0][1]]])
                    else:
                        # find all occurrences of atom_indices pairs
                        list_indices = [i for i, x in enumerate(adjacency_list) if x == selected_atom_indices]

                        # iterate through all entries with the same atom indices pairs
                        correct_list_index = None
                        for list_index in list_indices:
                            # if there is an entry that corresponds to the same type of donor-acceptor interaction
                            # set correct index to append to.
                            if nbo_types[list_index] == [donor_nbo_type, acceptor_nbo_type]:
                                correct_list_index = list_index
                                break

                        # if there does not exist an interaction between these kinds of NBOs make a new entry
                        if correct_list_index is None:
                            adjacency_list.append(selected_atom_indices)
                            stabilisation_energies.append([qm_data.sopa_data[i][1][0]])
                            nbo_types.append([donor_nbo_type, acceptor_nbo_type])
                            nbo_ids.append([[qm_data.sopa_data[i][0][0], qm_data.sopa_data[i][0][1]]])
                        # otherwise append to the existing entry
                        else:
                            stabilisation_energies[correct_list_index].append(qm_data.sopa_data[i][1][0])
                            nbo_ids[correct_list_index].append([qm_data.sopa_data[i][0][0], qm_data.sopa_data[i][0][1]])

        # make sure that lists have the same length
        assert len(adjacency_list) == len(stabilisation_energies)
        assert len(adjacency_list) == len(nbo_types)
        assert len(adjacency_list) == len(nbo_ids)

        return adjacency_list, stabilisation_energies, nbo_ids

    def _get_sopa_edges(self, qm_data: QmData) -> list[Edge]:

        """Generates a set of edges based on SOPA data.

        Returns:
            list[Edge]: List of edges.
        """

        # obtain SOPA adjacency list and associated stabilisation energies and NBO types
        adjacency_list, stabilisation_energies, nbo_ids = self._get_sopa_adjacency_list(qm_data)
        # format nbo_ids and stabilisation energies according to specification
        resolved_nbo_ids = self._resolve_nbo_ids(stabilisation_energies, nbo_ids, self._settings.sopa_resolution_mode)
        resolved_stabilisation_energies = self._resolve_stabilisation_energies(stabilisation_energies, self._settings.sopa_resolution_mode)

        edges = []
        for i in range(len(adjacency_list)):
            for j in range(len(resolved_stabilisation_energies[i])):

                # skip if stabilisation energy is less than specified interaction threshold
                if resolved_stabilisation_energies[i][j] < self._settings.sopa_interaction_threshold:
                    continue

                # set up feature list with stabilisation energy and NBO types
                features = self._get_sopa_edge_features(qm_data, stabilisation_energies[i], nbo_ids[i], resolved_nbo_ids[i][j])
                # add additional features
                features = features | self._get_edge_features(adjacency_list[i], qm_data)

                # set edge id and label
                edge_label = 'SOPA'
                edge_id = 'sopa-' + str(i)

                edges.append(Edge(adjacency_list[i], features=features, is_directed=True, label=edge_label, id=edge_id))

        return edges

    def _get_sopa_edge_features(self, qm_data: QmData, stabilisation_energies: list[list[float]], same_type_nbo_ids: list[list[int]], nbo_ids: list[list[int]]) -> list[float]:

        """Gets the SOPA edge features for given atom indices according to specification.

        Returns:
            list[float]: A list of SOPA edge features.
        """

        # obtain SOPA adjacency list and associated stabilisation energies and NBO types
        # adjacency_list, stabilisation_energies, nbo_types = self._get_sopa_adjacency_list(qm_data)

        # get donor and acceptor NBO data points
        donor_nbo = self._get_nbo_from_nbo_id(qm_data, nbo_ids[0])
        acceptor_nbo = self._get_nbo_from_nbo_id(qm_data, nbo_ids[1])

        # setup edge_features
        edge_features = {}

        # stabilisation energy features
        if SopaEdgeFeature.STABILISATION_ENERGY_MAX in self._settings.sopa_edge_features:
            edge_features['stabilisation_energy_max'] = max(stabilisation_energies)

        if SopaEdgeFeature.STABILISATION_ENERGY_AVERAGE in self._settings.sopa_edge_features:
            edge_features['stabilisation_energy_average'] = mean(stabilisation_energies)

        # donor features
        if SopaEdgeFeature.DONOR_NBO_TYPE in self._settings.sopa_edge_features:
            edge_features['donor_nbo_type'] = donor_nbo.nbo_type

        if SopaEdgeFeature.DONOR_NBO_ENERGY in self._settings.sopa_edge_features:
            edge_features['donor_nbo_energy'] = donor_nbo.energy

        if SopaEdgeFeature.DONOR_NBO_MIN_MAX_ENERGY_GAP in self._settings.sopa_edge_features:
            same_type_donor_nbo_energies = [self._get_nbo_from_nbo_id(qm_data, same_type_nbo_id[0]).energy for same_type_nbo_id in same_type_nbo_ids]
            edge_features['donor_nbo_min_max_energy_gap'] = max(same_type_donor_nbo_energies) - min(same_type_donor_nbo_energies)

        if SopaEdgeFeature.DONOR_NBO_OCCUPATION in self._settings.sopa_edge_features:
            edge_features['donor_nbo_occupation'] = donor_nbo.occupation

        for k in self._settings.donor_orbital_indices:
            edge_features['donor_nbo_' + ['s', 'p','d', 'f'][k] + '_occupation'] = donor_nbo.orbital_occupations[k]

        # acceptor features
        if SopaEdgeFeature.ACCEPTOR_NBO_TYPE in self._settings.sopa_edge_features:
            edge_features['acceptor_nbo_type'] = acceptor_nbo.nbo_type

        if SopaEdgeFeature.ACCEPTOR_NBO_ENERGY in self._settings.sopa_edge_features:
            edge_features['acceptor_nbo_energy'] = acceptor_nbo.energy

        if SopaEdgeFeature.ACCEPTOR_NBO_MIN_MAX_ENERGY_GAP in self._settings.sopa_edge_features:
            same_type_acceptor_nbo_energies = [self._get_nbo_from_nbo_id(qm_data, same_type_nbo_id[1]).energy for same_type_nbo_id in same_type_nbo_ids]
            edge_features['acceptor_nbo_min_max_energy_gap'] = max(same_type_acceptor_nbo_energies) - min(same_type_acceptor_nbo_energies)

        if SopaEdgeFeature.ACCEPTOR_NBO_OCCUPATION in self._settings.sopa_edge_features:
            edge_features['acceptor_nbo_occupation'] = acceptor_nbo.occupation

        for k in self._settings.acceptor_orbital_indices:
            edge_features['acceptor_nbo_' + ['s', 'p','d', 'f'][k] + '_occupation'] = acceptor_nbo.orbital_occupations[k]

        return edge_features

    def _resolve_nbo_ids(self, stabilisation_energies: list[list[float]], nbo_ids: list[list[int]], mode: SopaResolutionMode) -> list[list[int]]:

        """Helper function to resolve a list of NBO ids based on the stabilisation energies and according to the SOPA mode specification.

        Returns:
            list[list[float]]: List of lists containing the stabilisation energies.
        """

        resolved_nbo_ids = []

        # keeps all individual stabilisation energies
        if mode == SopaResolutionMode.FULL:
            return nbo_ids
        # averages over stabilisation energies belonging to the same atom pair
        elif mode == SopaResolutionMode.AVERAGE:
            raise ValueError('Cannot average-resolve NBO IDs.')
        # uses the minimum and maximum values of stabilisation energies belonging to the same atom pair
        elif mode == SopaResolutionMode.MIN_MAX:
            for i in range(len(stabilisation_energies)):
                if len(stabilisation_energies[i]) == 1:
                    resolved_nbo_ids.append(nbo_ids[i])
                else:
                    # get lists of indices in case the max or min value are degenerate
                    min_indices = [j for j, x in enumerate(stabilisation_energies[i]) if x == min(stabilisation_energies[i])]
                    max_indices = [j for j, x in enumerate(stabilisation_energies[i]) if x == max(stabilisation_energies[i])]
                    unique_indices = list(set(min_indices + max_indices))
                    min_max_energy_nbo_ids = [nbo_ids[i][idx] for idx in unique_indices]
                    resolved_nbo_ids.append(min_max_energy_nbo_ids)
        # gets the NBO IDs corresponding to maximum value of stabilisation energies belonging to the same atom pair
        elif mode == SopaResolutionMode.MAX:
            for i in range(len(stabilisation_energies)):
                max_indices = [j for j, x in enumerate(stabilisation_energies[i]) if x == max(stabilisation_energies[i])]
                max_energy_nbo_ids = [nbo_ids[i][idx] for idx in max_indices]
                resolved_nbo_ids.append(max_energy_nbo_ids)
        # gets the NBO IDs corresponding to the minimum value of stabilisation energies belonging to the same atom pair
        elif mode == SopaResolutionMode.MIN:
            for i in range(len(stabilisation_energies)):
                min_indices = [j for j, x in enumerate(stabilisation_energies[i]) if x == min(stabilisation_energies[i])]
                min_energy_nbo_ids = [nbo_ids[i][idx] for idx in min_indices]
                resolved_nbo_ids.append(min_energy_nbo_ids)

        return resolved_nbo_ids

    def _resolve_stabilisation_energies(self, stabilisation_energies: list[list[float]], mode: SopaResolutionMode) -> list[list[float]]:

        """Helper function to resolve a list of stabilisation energies according to the SOPA mode specification.

        Returns:
            list[list[float]]: List of lists containing the stabilisation energies.
        """

        resolved_stabilisation_energies = []

        # keeps all individual stabilisation energies
        if mode == SopaResolutionMode.FULL:
            return stabilisation_energies
        # averages over stabilisation energies belonging to the same atom pair
        elif mode == SopaResolutionMode.AVERAGE:
            for i in range(len(stabilisation_energies)):
                resolved_stabilisation_energies.append([mean(stabilisation_energies[i])])
        # uses the minimum and maximum values of stabilisation energies belonging to the same atom pair
        elif mode == SopaResolutionMode.MIN_MAX:
            for i in range(len(stabilisation_energies)):
                if len(stabilisation_energies[i]) == 1:
                    resolved_stabilisation_energies.append(stabilisation_energies[i])
                else:
                    # get lists of indices in case the max or min value are degenerate
                    min_indices = [j for j, x in enumerate(stabilisation_energies[i]) if x == min(stabilisation_energies[i])]
                    max_indices = [j for j, x in enumerate(stabilisation_energies[i]) if x == max(stabilisation_energies[i])]
                    unique_indices = list(set(min_indices + max_indices))
                    min_max_energies = [stabilisation_energies[i][idx] for idx in unique_indices]
                    resolved_stabilisation_energies.append(min_max_energies)
        # uses the maximum value of stabilisation energies belonging to the same atom pair
        elif mode == SopaResolutionMode.MAX:
            for i in range(len(stabilisation_energies)):
                max_indices = [j for j, x in enumerate(stabilisation_energies[i]) if x == max(stabilisation_energies[i])]
                max_energies = [stabilisation_energies[i][idx] for idx in max_indices]
                resolved_stabilisation_energies.append(max_energies)
        # uses the minimum value of stabilisation energies belonging to the same atom pair
        elif mode == SopaResolutionMode.MIN:
            for i in range(len(stabilisation_energies)):
                min_indices = [j for j, x in enumerate(stabilisation_energies[i]) if x == min(stabilisation_energies[i])]
                min_energies = [stabilisation_energies[i][idx] for idx in min_indices]
                resolved_stabilisation_energies.append(min_energies)

        return resolved_stabilisation_energies

    def _get_meta_data(self, qm_data: QmData):

        # set up variable to hold the number of individual atoms
        element_counts = {}

        for atomic_number in qm_data.atomic_numbers:

            # increment element count by one
            current_element = ElementLookUpTable.get_element_identifier(atomic_number)
            if current_element in element_counts.keys():
                element_counts[current_element] += 1
            else:
                element_counts[current_element] = 1

            # determine center element
            if atomic_number in ElementLookUpTable.transition_metal_atomic_numbers:
                metal_center_element = current_element

        meta_data = {
            'id': qm_data.id,
            'n_atoms': qm_data.n_atoms,
            'n_electrons': (sum(qm_data.atomic_numbers) - qm_data.charge),
            'metal_center_element': metal_center_element,
            'metal_center_group': ElementLookUpTable.atom_format_dict[metal_center_element]['group'],
            'metal_center_period': ElementLookUpTable.atom_format_dict[metal_center_element]['period'],
            'element_counts': element_counts
        }

        return meta_data
