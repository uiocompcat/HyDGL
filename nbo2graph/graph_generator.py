import warnings
from statistics import mean

from nbo2graph.node import Node
from nbo2graph.edge import Edge
from nbo2graph.graph import Graph
from nbo2graph.qm_data import QmData
from nbo2graph.enums.qm_target import QmTarget
from nbo2graph.enums.edge_feature import EdgeFeature
from nbo2graph.enums.node_feature import NodeFeature
from nbo2graph.enums.hydrogen_mode import HydrogenMode
from nbo2graph.enums.graph_feature import GraphFeature
from nbo2graph.element_look_up_table import ElementLookUpTable
from nbo2graph.nbo_single_data_point import NboSingleDataPoint
from nbo2graph.nbo_double_data_point import NboDoubleDataPoint
from nbo2graph.enums.sopa_resolution_mode import SopaResolutionMode
from nbo2graph.graph_generator_settings import GraphGeneratorSettings
from nbo2graph.enums.bond_determination_mode import BondDeterminationMode


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
        edges = self._get_sopa_edges(qm_data)
        # edges = self._get_edges(qm_data)

        # rescale node referenes in edges if explicit hydrogens were omitted
        if self._settings.hydrogen_mode == HydrogenMode.OMIT or self._settings.hydrogen_mode == HydrogenMode.IMPLICIT:
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
                     targets=targets,
                     graph_features=graph_features,
                     id=qm_data.id,
                     stoichiometry=qm_data.stoichiometry)

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

        # operations only relevant when not modelling hydrogens explicitly
        if self._settings.hydrogen_mode == HydrogenMode.OMIT or self._settings.hydrogen_mode == HydrogenMode.IMPLICIT:

            # check for hydride hydrogens to add explicitly
            hydride_bond_indices = self._get_hydride_bond_indices(qm_data)
            for i in range(len(hydride_bond_indices)):
                edges.append(self._get_featurised_edge(hydride_bond_indices[i], qm_data))

        return edges

    def _get_adjacency_list(self, qm_data: QmData) -> list[list[int]]:

        adjacency_list = []

        if self._settings.bond_determination_mode == BondDeterminationMode.NBO_BONDING_ORBITALS:

            for i in range(len(qm_data.bond_pair_data)):
                # ignore hydrogens in omit and implicit mode
                if self._settings.hydrogen_mode == HydrogenMode.OMIT or self._settings.hydrogen_mode == HydrogenMode.IMPLICIT:
                    if qm_data.atomic_numbers[qm_data.bond_pair_data[i].atom_indices[0]] == 1 or qm_data.atomic_numbers[qm_data.bond_pair_data[i].atom_indices[1]] == 1:
                        continue

                if not qm_data.bond_pair_data[i].atom_indices in adjacency_list:
                    adjacency_list.append(qm_data.bond_pair_data[i].atom_indices)

            return sorted(adjacency_list)
        else:
            # get appropriate index matrix
            index_matrix = self._get_index_matrix(qm_data)

            # iterate over half triangle matrix to determine bonds
            for i in range(len(index_matrix) - 1):

                for j in range(i + 1, len(index_matrix), 1):

                    # decide which threshold to use
                    if qm_data.atomic_numbers[i] in ElementLookUpTable.transition_metal_atomic_numbers or qm_data.atomic_numbers[j] in ElementLookUpTable.transition_metal_atomic_numbers:
                        threshold = self._settings.bond_threshold_metal
                    else:
                        threshold = self._settings.bond_threshold

                    # if larger than threshold --> add bond
                    if (index_matrix[i][j]) > threshold:

                        # append the atom indices (pos 0)
                        # and Wiberg bond index as a feature (pos 1)

                        # ignore hydrogens in omit and implicit mode
                        if self._settings.hydrogen_mode == HydrogenMode.OMIT or self._settings.hydrogen_mode == HydrogenMode.IMPLICIT:
                            if qm_data.atomic_numbers[i] == 1 or qm_data.atomic_numbers[j] == 1:
                                continue

                        # append edge with empty feature vector
                        adjacency_list.append([i, j])

            return adjacency_list

    def _get_featurised_edge(self, bond_atom_indices: list[int], qm_data: QmData) -> Edge:

        # pre read data for efficiency

        # bonds with BD and BD*
        bond_pair_atom_indices = [x.atom_indices for x in qm_data.bond_pair_data]
        antibond_pair_atom_indices = [x.atom_indices for x in qm_data.antibond_pair_data]

        # corresponding energy values
        bond_pair_energies = [x.energy for x in qm_data.bond_pair_data]
        antibond_pair_energies = [x.energy for x in qm_data.antibond_pair_data]

        # setup edge_features
        edge_features = []

        # append requested bond orders
        if EdgeFeature.WIBERG_BOND_ORDER in self._settings.edge_features:
            edge_features.append(qm_data.wiberg_bond_order_matrix[bond_atom_indices[0]][bond_atom_indices[1]])
        if EdgeFeature.LMO_BOND_ORDER in self._settings.edge_features:
            edge_features.append(qm_data.lmo_bond_order_matrix[bond_atom_indices[0]][bond_atom_indices[1]])
        if EdgeFeature.NLMO_BOND_ORDER in self._settings.edge_features:
            edge_features.append(qm_data.nlmo_bond_order_matrix[bond_atom_indices[0]][bond_atom_indices[1]])

        # add bond distance as feature to edges
        if EdgeFeature.BOND_DISTANCE in self._settings.edge_features:
            edge_features.append(qm_data.bond_distance_matrix[bond_atom_indices[0]][bond_atom_indices[1]])

        # add number of bond/antibond orbitals if requested
        if EdgeFeature.BOND_ORBITAL_MAX in self._settings.edge_features or \
                EdgeFeature.BOND_ORBITAL_AVERAGE in self._settings.edge_features or \
                EdgeFeature.ANTIBOND_ORBITAL_MIN in self._settings.edge_features or \
                EdgeFeature.ANTIBOND_ORBITAL_AVERAGE in self._settings.edge_features or \
                EdgeFeature.BOND_ENERGY_MIN_MAX_DIFFERENCE in self._settings.edge_features or \
                EdgeFeature.ANTIBOND_ENERGY_MIN_MAX_DIFFERENCE in self._settings.edge_features:

            if bond_atom_indices in bond_pair_atom_indices:
                # length of bond pair list for this edge
                edge_features.append(len([x.energy for x in qm_data.bond_pair_data if x.atom_indices == bond_atom_indices]))
            else:
                edge_features.append(0)

        if EdgeFeature.BOND_ENERGY_MIN_MAX_DIFFERENCE in self._settings.edge_features:
            energies = [x.energy for x in qm_data.bond_pair_data if x.atom_indices == bond_atom_indices]

            # append difference if there are 2 entries or more
            if len(energies) >= 2:
                edge_features.append(abs(min(energies) - max(energies)))
            # append 0 otherwise
            else:
                edge_features.append(0.0)

        if EdgeFeature.BOND_ORBITAL_MAX in self._settings.edge_features and len(self._settings.bond_orbital_indices) > 0:

            # check if NBO data for the respective bond is available
            # if so add to feature vector
            # otherwise add zeros to feature vector
            if bond_atom_indices in bond_pair_atom_indices:

                # get list of all bond pair energies for this atom
                energies = [x.energy for x in qm_data.bond_pair_data if x.atom_indices == bond_atom_indices]

                # select index of the highest energy (for BD)
                selected_index = bond_pair_energies.index(max(energies))

                # append data (total length = 2 + number of orbital occupancies)
                edge_features.append(qm_data.bond_pair_data[selected_index].energy)
                edge_features.append(qm_data.bond_pair_data[selected_index].occupation)
                edge_features.extend([qm_data.bond_pair_data[selected_index].orbital_occupations[k] for k in self._settings.bond_orbital_indices])

            else:
                edge_features.extend((2 + len(self._settings.bond_orbital_indices)) * [0.0])

        if EdgeFeature.BOND_ORBITAL_AVERAGE in self._settings.edge_features and len(self._settings.bond_orbital_indices) > 0:
            # check if NBO data for the respective bonds is available
            # if so add to feature vector
            # otherwise add zeros to feature vector
            if bond_atom_indices in bond_pair_atom_indices:

                # get list of all antibond pair energies for this atom
                energies = [x.energy for x in qm_data.bond_pair_data if x.atom_indices == bond_atom_indices]
                # get list of all occupation values for this atom
                occupations = [x.occupation for x in qm_data.bond_pair_data if x.atom_indices == bond_atom_indices]
                # get list of symmetry values of different lone pairs for this atom
                symmetries = [x.orbital_occupations for x in qm_data.bond_pair_data if x.atom_indices == bond_atom_indices]

                # append average values for energies and occupations
                edge_features.append(mean(energies))
                edge_features.append(mean(occupations))

                # get average values for orbital symmetries
                oribtal_symmetries = [mean(x) for x in [[y[k] for y in symmetries] for k in self._settings.bond_orbital_indices]]
                edge_features.extend(oribtal_symmetries)
            else:
                edge_features.extend((2 + len(self._settings.bond_orbital_indices)) * [0.0])

        if EdgeFeature.ANTIBOND_ENERGY_MIN_MAX_DIFFERENCE in self._settings.edge_features:
            energies = [x.energy for x in qm_data.antibond_pair_data if x.atom_indices == bond_atom_indices]

            # append difference if there are 2 entries or more
            if len(energies) >= 2:
                edge_features.append(abs(min(energies) - max(energies)))
            # append 0 otherwise
            else:
                edge_features.append(0.0)

        if EdgeFeature.ANTIBOND_ORBITAL_MIN in self._settings.edge_features and len(self._settings.antibond_orbital_indices) > 0:
            # check if NBO data for the respective antibonds is available
            # if so add to feature vector
            # otherwise add zeros to feature vector
            if bond_atom_indices in antibond_pair_atom_indices:

                # get list of all antibond pair energies for this atom
                energies = [x.energy for x in qm_data.antibond_pair_data if x.atom_indices == bond_atom_indices]

                # select index of the lowest energy (for BD*)
                selected_index = antibond_pair_energies.index(min(energies))

                # append data (total length = 2 + number of orbital occupancies)
                edge_features.append(qm_data.antibond_pair_data[selected_index].energy)
                edge_features.append(qm_data.antibond_pair_data[selected_index].occupation)
                edge_features.extend([qm_data.bond_pair_data[selected_index].orbital_occupations[k] for k in self._settings.antibond_orbital_indices])
            else:
                edge_features.extend((2 + len(self._settings.antibond_orbital_indices)) * [0.0])

        if EdgeFeature.ANTIBOND_ORBITAL_AVERAGE in self._settings.edge_features and len(self._settings.antibond_orbital_indices) > 0:
            # check if NBO data for the respective antibonds is available
            # if so add to feature vector
            # otherwise add zeros to feature vector
            if bond_atom_indices in antibond_pair_atom_indices:

                # get list of all antibond pair energies for this atom
                energies = [x.energy for x in qm_data.antibond_pair_data if x.atom_indices == bond_atom_indices]
                # get list of all occupation values for this atom
                occupations = [x.occupation for x in qm_data.antibond_pair_data if x.atom_indices == bond_atom_indices]
                # get list of symmetry values of different lone pairs for this atom
                symmetries = [x.orbital_occupations for x in qm_data.antibond_pair_data if x.atom_indices == bond_atom_indices]

                # append average values for energies and occupations
                edge_features.append(mean(energies))
                edge_features.append(mean(occupations))

                # get average values for orbital symmetries
                oribtal_symmetries = [mean(x) for x in [[y[k] for y in symmetries] for k in self._settings.antibond_orbital_indices]]
                edge_features.extend(oribtal_symmetries)
            else:
                edge_features.extend((2 + len(self._settings.antibond_orbital_indices)) * [0.0])

        return Edge(bond_atom_indices, features=edge_features)

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
            if self._settings.hydrogen_mode == HydrogenMode.OMIT or self._settings.hydrogen_mode == HydrogenMode.IMPLICIT:
                if qm_data.atomic_numbers[i] == 1:
                    continue

            node_indices.append(i)

        # operations only relevant when not modelling hydrogens explicitly
        if self._settings.hydrogen_mode == HydrogenMode.OMIT or self._settings.hydrogen_mode == HydrogenMode.IMPLICIT:

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
        lone_pair_atom_indices = [x.atom_index for x in qm_data.lone_pair_data]
        lone_vacancy_atom_indices = [x.atom_index for x in qm_data.lone_vacancy_data]

        # corresponding energy values
        lone_pair_energies = [x.energy for x in qm_data.lone_pair_data]
        lone_vacancy_energies = [x.energy for x in qm_data.lone_vacancy_data]

        # set up features for node
        node_features = []

        # add atomic number
        if NodeFeature.ATOMIC_NUMBERS in self._settings.node_features:
            node_features.append(qm_data.atomic_numbers[i])

        # add natural atomic charge
        if NodeFeature.NATURAL_ATOMIC_CHARGES in self._settings.node_features:
            node_features.append(qm_data.natural_atomic_charges[i])

        # add natural electron configuration (requested orbital occupancies)
        if len(self._settings.natural_orbital_configuration_indices) > 0:
            node_features.extend([qm_data.natural_electron_configuration[i][k] for k in self._settings.natural_orbital_configuration_indices])

        # add bond order totals

        # Wiberg mode
        if NodeFeature.WIBERG_BOND_ORDER_TOTAL in self._settings.node_features:
            node_features.append(qm_data.wiberg_bond_order_totals[i])
        # LMO mode
        if NodeFeature.LMO_BOND_ORDER_TOTAL in self._settings.node_features:
            node_features.append(qm_data.lmo_bond_order_matrix[i])
        # NLMO mode
        if NodeFeature.NLMO_BOND_ORDER_TOTAL in self._settings.node_features:
            node_features.append(qm_data.nlmo_bond_order_totals[i])

        # add number of lone pairs if requested
        if NodeFeature.LONE_PAIR_MAX in self._settings.node_features or \
                NodeFeature.LONE_PAIR_AVERAGE in self._settings.node_features or \
                NodeFeature.LONE_PAIR_ENERGY_MIN_MAX_DIFFERENCE in self._settings.node_features:

            node_features.append(len([x.energy for x in qm_data.lone_pair_data if x.atom_index == i]))

        if NodeFeature.LONE_PAIR_ENERGY_MIN_MAX_DIFFERENCE in self._settings.node_features:
            energies = [x.energy for x in qm_data.lone_pair_data if x.atom_index == i]

            # append difference if there are 2 entries or more
            if len(energies) >= 2:
                node_features.append(abs(min(energies) - max(energies)))
            # append 0 otherwise
            else:
                node_features.append(0.0)

        if NodeFeature.LONE_PAIR_MAX in self._settings.node_features and len(self._settings.lone_pair_orbital_indices) > 0:
            if i in lone_pair_atom_indices:

                # get list of all lone pair energies for this atom
                energies = [x.energy for x in qm_data.lone_pair_data if x.atom_index == i]
                # select index of the highest energy (for LP)
                selected_index = lone_pair_energies.index(max(energies))

                # append data (total length = 4)
                node_features.append(qm_data.lone_pair_data[selected_index].energy)
                node_features.append(qm_data.lone_pair_data[selected_index].occupation)

                # get orbital occupations
                oribtal_symmetries = [qm_data.lone_pair_data[selected_index].orbital_occupations[k] for k in self._settings.lone_pair_orbital_indices]
                node_features.extend(oribtal_symmetries)
            else:
                node_features.extend((2 + len(self._settings.lone_pair_orbital_indices)) * [0.0])

        if NodeFeature.LONE_PAIR_AVERAGE in self._settings.node_features and len(self._settings.lone_pair_orbital_indices) > 0:
            if i in lone_pair_atom_indices:

                # get list of all lone pair energies for this atom
                energies = [x.energy for x in qm_data.lone_pair_data if x.atom_index == i]
                # get list of all lone pair occupations for this atom
                occupations = [x.occupation for x in qm_data.lone_pair_data if x.atom_index == i]
                # get list of symmetry values of different lone pairs for this atom
                symmetries = [x.orbital_occupations for x in qm_data.lone_pair_data if x.atom_index == i]

                # append average values for energies and occupations
                node_features.append(mean(energies))
                node_features.append(mean(occupations))

                # get average values for orbital symmetries
                oribtal_symmetries = [mean(x) for x in [[y[k] for y in symmetries] for k in self._settings.lone_pair_orbital_indices]]
                node_features.extend(oribtal_symmetries)
            else:
                node_features.extend((2 + len(self._settings.lone_pair_orbital_indices)) * [0.0])

        # add number of lone vacancies if requested
        if NodeFeature.LONE_VACANCY_MIN in self._settings.node_features or \
                NodeFeature.LONE_VACANCY_AVERAGE in self._settings.node_features or \
                NodeFeature.LONE_VACANCY_ENERGY_MIN_MAX_DIFFERENCE in self._settings.node_features:

            node_features.append(len([x.energy for x in qm_data.lone_vacancy_data if x.atom_index == i]))

        if NodeFeature.LONE_VACANCY_ENERGY_MIN_MAX_DIFFERENCE in self._settings.node_features:
            energies = [x.energy for x in qm_data.lone_vacancy_data if x.atom_index == i]

            # append difference if there are 2 entries or more
            if len(energies) >= 2:
                node_features.append(abs(min(energies) - max(energies)))
            # append 0 otherwise
            else:
                node_features.append(0.0)

        if NodeFeature.LONE_VACANCY_MIN in self._settings.node_features and len(self._settings.lone_vacancy_orbital_indices) > 0:
            if i in lone_vacancy_atom_indices:

                # get list of all lone pair energies for this atom
                energies = [x.energy for x in qm_data.lone_vacancy_data if x.atom_index == i]
                # select index of the lowest energy (for LV)
                selected_index = lone_vacancy_energies.index(min(energies))

                # append data (total length = 4)
                node_features.append(qm_data.lone_vacancy_data[selected_index].energy)
                node_features.append(qm_data.lone_vacancy_data[selected_index].occupation)

                # get orbital occupations
                oribtal_symmetries = [qm_data.lone_vacancy_data[selected_index].orbital_occupations[k] for k in self._settings.lone_vacancy_orbital_indices]
                node_features.extend(oribtal_symmetries)
            else:
                node_features.extend((2 + len(self._settings.lone_vacancy_orbital_indices)) * [0.0])

        if NodeFeature.LONE_VACANCY_AVERAGE in self._settings.node_features and len(self._settings.lone_vacancy_orbital_indices) > 0:
            if i in lone_vacancy_atom_indices:

                # get list of all lone pair energies for this atom
                energies = [x.energy for x in qm_data.lone_vacancy_data if x.atom_index == i]
                # get list of all lone pair occupations for this atom
                occupations = [x.occupation for x in qm_data.lone_vacancy_data if x.atom_index == i]
                # get list of symmetry values of different lone pairs for this atom
                symmetries = [x.orbital_occupations for x in qm_data.lone_vacancy_data if x.atom_index == i]

                # append average values for energies and occupations
                node_features.append(mean(energies))
                node_features.append(mean(occupations))

                # get average values for orbital symmetries
                oribtal_symmetries = [mean(x) for x in [[y[k] for y in symmetries] for k in self._settings.lone_vacancy_orbital_indices]]
                node_features.extend(oribtal_symmetries)
            else:
                node_features.extend((2 + len(self._settings.lone_vacancy_orbital_indices)) * [0.0])

        # add implicit hydrogens
        if self._settings.hydrogen_mode == HydrogenMode.IMPLICIT:
            # get hydrogen count for heavy atoms in implicit mode
            hydrogen_count = None
            if self._settings.hydrogen_mode == HydrogenMode.IMPLICIT:
                # set hydrogen count of hydrogens to 0
                if qm_data.atomic_numbers[i] == 1:
                    hydrogen_count = 0
                # set hydrogen count to 0 if transition metal (will be modelled explicitly)
                elif qm_data.atomic_numbers[i] in ElementLookUpTable.transition_metal_atomic_numbers:
                    hydrogen_count = 0
                # otherwise determine hydrogen count normally
                else:
                    hydrogen_count = self._determine_hydrogen_count(i, qm_data)

            node_features.append(hydrogen_count)

        if include_misc_data:
            # get node label and position
            node_label = ElementLookUpTable.get_element_identifier(qm_data.atomic_numbers[i])
            node_position = qm_data.geometric_data[i]

            return Node(features=node_features, position=node_position, label=node_label)
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
        index_matrix = self._get_index_matrix(qm_data)

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

    def _get_index_matrix(self, qm_data: QmData) -> list[list[float]]:

        """Helper function that returns the appropriate index matrix based on the GraphGenerator settings.

        Raises:
            ValueError: If a bond determination mode is selected that can not be resolved.

        Returns:
            list[list[float]]: The selected index matrix.
        """

        # decide which index matrix to return

        # Wiberg mode
        if self._settings.bond_determination_mode == BondDeterminationMode.WIBERG:
            return qm_data.wiberg_bond_order_matrix
        # LMO mode
        elif self._settings.bond_determination_mode == BondDeterminationMode.LMO:
            return qm_data.lmo_bond_order_matrix
        # NLMO mode
        elif self._settings.bond_determination_mode == BondDeterminationMode.NLMO:
            return qm_data.nlmo_bond_order_matrix
        # raise exception otherwise
        else:
            print('Bond determination mode not recognised. Defaulting to Wiberg')
            return qm_data.wiberg_bond_order_matrix

    def _get_graph_features(self, qm_data: QmData) -> list:

        """Function to return the requested graph features.

        Returns:
            list[float]: A list of requested graph features.
        """

        # return variable
        graph_feature_list = []

        for i in range(len(self._settings.graph_features)):

            if self._settings.graph_features[i] == GraphFeature.N_ATOMS:
                graph_feature_list.append(qm_data.n_atoms)
            elif self._settings.graph_features[i] == GraphFeature.MOLECULAR_MASS:
                graph_feature_list.append(qm_data.molecular_mass)
            elif self._settings.graph_features[i] == GraphFeature.CHARGE:
                graph_feature_list.append(qm_data.charge)
            else:
                warnings.warn('Could not find target' + str(self._settings.graph_features[i]) + '.')

        return graph_feature_list

    def _get_targets(self, qm_data: QmData) -> list[float]:

        """Helper function to resolve which targets to use.

        Returns:
            list[float]: List of graph targets.
        """

        # return variable
        target_list = []

        for i in range(len(self._settings.targets)):

            if type(self._settings.targets[i]) is not QmTarget:
                warnings.warn('Element ' + str(i) + ' of list is not of type QmTarget. Entry will be skipped.')

            if self._settings.targets[i] == QmTarget.SVP_ELECTRONIC_ENERGY:
                target_list.append(qm_data.svp_electronic_energy)
            elif self._settings.targets[i] == QmTarget.TZVP_ELECTRONIC_ENERGY:
                target_list.append(qm_data.tzvp_electronic_energy)
            elif self._settings.targets[i] == QmTarget.SVP_DISPERSION_ENERGY:
                target_list.append(qm_data.svp_dispersion_energy)
            elif self._settings.targets[i] == QmTarget.TZVP_DISPERSION_ENERGY:
                target_list.append(qm_data.tzvp_dispersion_energy)
            elif self._settings.targets[i] == QmTarget.SVP_DIPOLE_MOMENT:
                target_list.append(qm_data.svp_dipole_moment)
            elif self._settings.targets[i] == QmTarget.TZVP_DIPOLE_MOMENT:
                target_list.append(qm_data.tzvp_dipole_moment)
            elif self._settings.targets[i] == QmTarget.SVP_HOMO_ENERGY:
                target_list.append(qm_data.svp_homo_energy)
            elif self._settings.targets[i] == QmTarget.TZVP_HOMO_ENERGY:
                target_list.append(qm_data.tzvp_homo_energy)
            elif self._settings.targets[i] == QmTarget.SVP_LUMO_ENERGY:
                target_list.append(qm_data.svp_lumo_energy)
            elif self._settings.targets[i] == QmTarget.TZVP_LUMO_ENERGY:
                target_list.append(qm_data.tzvp_lumo_energy)
            elif self._settings.targets[i] == QmTarget.SVP_HOMO_LUMO_GAP:
                target_list.append(qm_data.svp_homo_lumo_gap)
            elif self._settings.targets[i] == QmTarget.TZVP_HOMO_LUMO_GAP:
                target_list.append(qm_data.tzvp_homo_lumo_gap)
            elif self._settings.targets[i] == QmTarget.LOWEST_VIBRATIONAL_FREQUENCY:
                target_list.append(qm_data.lowest_vibrational_frequency)
            elif self._settings.targets[i] == QmTarget.HIGHEST_VIBRATIONAL_FREQUENCY:
                target_list.append(qm_data.highest_vibrational_frequency)
            elif self._settings.targets[i] == QmTarget.HEAT_CAPACITY:
                target_list.append(qm_data.heat_capacity)
            elif self._settings.targets[i] == QmTarget.ENTROPY:
                target_list.append(qm_data.entropy)
            elif self._settings.targets[i] == QmTarget.ZPE_CORRECTION:
                target_list.append(qm_data.zpe_correction)
            elif self._settings.targets[i] == QmTarget.ENTHALPY_ENERGY:
                target_list.append(qm_data.enthalpy_energy)
            elif self._settings.targets[i] == QmTarget.GIBBS_ENERGY:
                target_list.append(qm_data.gibbs_energy)
            elif self._settings.targets[i] == QmTarget.CORRECTED_ENTHALPY_ENERGY:
                target_list.append(qm_data.corrected_enthalpy_energy)
            elif self._settings.targets[i] == QmTarget.CORRECTED_GIBBS_ENERGY:
                target_list.append(qm_data.corrected_gibbs_energy)
            elif self._settings.targets[i] == QmTarget.ELECTRONIC_ENERGY_DELTA:
                target_list.append(qm_data.electronic_energy_delta)
            elif self._settings.targets[i] == QmTarget.DISPERSION_ENERGY_DELTA:
                target_list.append(qm_data.dispersion_energy_delta)
            elif self._settings.targets[i] == QmTarget.DIPOLE_MOMENT_DELTA:
                target_list.append(qm_data.dipole_moment_delta)
            elif self._settings.targets[i] == QmTarget.HOMO_LUMO_GAP_DELTA:
                target_list.append(qm_data.homo_lumo_gap_delta)
            elif self._settings.targets[i] == QmTarget.POLARISABILITY:
                target_list.append(qm_data.polarisability)
            else:
                warnings.warn('Could not find target' + str(self._settings.targets[i]) + '.')

        return target_list

    def _validate_node_list(self, nodes: list[Node]):

        # check that all node vectors have the same length
        for i in range(1, len(nodes), 1):
            assert len(nodes[i].features) == len(nodes[0].features)

    def _validate_edge_list(self, edges: list[Edge], n_nodes: int):

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
        # if single data point return the index
        if type(qm_data.nbo_data[nbo_list_index]) == NboSingleDataPoint:
            return [qm_data.nbo_data[nbo_list_index].atom_index]
        # if double data point return both indices
        elif type(qm_data.nbo_data[nbo_list_index]) == NboDoubleDataPoint:
            return qm_data.nbo_data[nbo_list_index].atom_indices

    def _select_atom_indices_from_nbo_id(self, qm_data: QmData, nbo_id: int) -> list[int]:

        """Selects atom indices associated to a NBO ID based on their respective contributions.

        Returns:
            list[int]: A list of selected atom indices.
        """

        nbo_list_index = next((i for i, item in enumerate(qm_data.nbo_data) if item.nbo_id == nbo_id), -1)
        # if single data point simply return the index
        if type(qm_data.nbo_data[nbo_list_index]) == NboSingleDataPoint:
            return [qm_data.nbo_data[nbo_list_index].atom_index]
        # if double data point check contributions values
        elif type(qm_data.nbo_data[nbo_list_index]) == NboDoubleDataPoint:
            selected_atom_indices = []
            for i in range(len(qm_data.nbo_data[nbo_list_index].atom_indices)):
                if qm_data.nbo_data[nbo_list_index].contributions[i] > self._settings.sopa_contribution_threshold:
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

    def _get_sopa_adjacency_list(self, qm_data: QmData) -> list[list[int]]:

        """Gets an adjacency list based on SOPA data. Also returns list of associated stabilisation energies and NBO types.

        Returns:
            list[list[int]]: Adjacency list.
            list[list[floats]]: Corresponding lists of associated stabilisation energies.
            list[list[str]]: Corresponding lists of asscociated NBO types.
        """

        atom_indices_list = []
        stabilisation_energies = []
        nbo_types = []
        for i in range(len(qm_data.sopa_data)):

            # skip if nbo type is not one of: LP, LV, BD, BD*
            if next((j for j, item in enumerate(qm_data.nbo_data) if item.nbo_id == qm_data.sopa_data[i][0][0]), -1) == -1:
                continue
            if next((j for j, item in enumerate(qm_data.nbo_data) if item.nbo_id == qm_data.sopa_data[i][0][1]), -1) == -1:
                continue

            # get all atom indices involved in the two nbo entries
            donor_atom_indices = self._get_atom_indices_from_nbo_id(qm_data, qm_data.sopa_data[i][0][0])
            acceptor_atom_indices = self._get_atom_indices_from_nbo_id(qm_data, qm_data.sopa_data[i][0][1])

            # skip if it is a hydrogen interaction unless a metal is involved
            atom_indices_collection = donor_atom_indices + acceptor_atom_indices
            if self._contains_hydrogen(qm_data, atom_indices_collection) and not self._contains_metal(qm_data, atom_indices_collection):
                continue

            donor_nbo_type = self._get_nbo_type_from_nbo_id(qm_data, qm_data.sopa_data[i][0][0])
            acceptor_nbo_type = self._get_nbo_type_from_nbo_id(qm_data, qm_data.sopa_data[i][0][1])

            # get selected atom indices involved in two nbo entries
            donor_selected_atom_indices = self._select_atom_indices_from_nbo_id(qm_data, qm_data.sopa_data[i][0][0])
            acceptor_selected_atom_indices = self._select_atom_indices_from_nbo_id(qm_data, qm_data.sopa_data[i][0][1])

            # add bond indices for each combination of indeces
            for index_a in donor_selected_atom_indices:
                for index_b in acceptor_selected_atom_indices:

                    selected_atom_indices = [index_a, index_b]

                    # add selected atom indices if not already in list
                    if selected_atom_indices not in atom_indices_list:
                        atom_indices_list.append(selected_atom_indices)
                        stabilisation_energies.append([qm_data.sopa_data[i][1][0]])
                        nbo_types.append([donor_nbo_type, acceptor_nbo_type])
                    else:
                        # find all occurrences of atom_indices pairs
                        list_indices = [i for i, x in enumerate(atom_indices_list) if x == selected_atom_indices]

                        # find the correct index for this set of NBO types
                        correct_list_index = None
                        for list_index in list_indices:
                            if nbo_types[list_index] == [donor_nbo_type, acceptor_nbo_type]:
                                correct_list_index = list_index
                                break

                        if correct_list_index is None:
                            atom_indices_list.append(selected_atom_indices)
                            stabilisation_energies.append([qm_data.sopa_data[i][1][0]])
                            nbo_types.append([donor_nbo_type, acceptor_nbo_type])
                        else:
                            stabilisation_energies[list_index].append(qm_data.sopa_data[i][1][0])

        # make sure that lists have the same length
        assert len(atom_indices_list) == len(stabilisation_energies)
        assert len(atom_indices_list) == len(nbo_types)

        return atom_indices_list, stabilisation_energies, nbo_types

    def _get_sopa_edges(self, qm_data: QmData) -> list[Edge]:

        """Generates a set of edges based on SOPA data.

        Returns:
            list[Edge]: List of edges.
        """

        # obtain SOPA adjacency list and associated stabilisation energies and NBO types
        atom_indices_list, stabilisation_energies, nbo_types = self._get_sopa_adjacency_list(qm_data)
        # format stabilisation energies according to specification
        stabilisation_energies = self._resolve_stabilisation_energies(stabilisation_energies)

        edges = []
        for i in range(len(atom_indices_list)):
            for j in range(len(stabilisation_energies[i])):

                # set up feature list with stabilisation energy and NBO types
                features = [stabilisation_energies[i][j]]
                features.extend(nbo_types[i])
                # here, additional features could be added to the feature list
                # features.extend()

                edges.append(Edge(atom_indices_list[i], features=features, is_directed=True))

        return edges

    def _resolve_stabilisation_energies(self, stabilisation_energies):

        """Helper function to resolve a list of stabilisation energies according to the specification.

        Returns:
            list[list[float]]: List of lists containing the stabilisation energies.
        """

        # keeps all individual stabilisation energies
        if self._settings.sopa_resolution_mode == SopaResolutionMode.FULL:
            pass
        # averages over stabilisation energies belonging to the same atom pair
        elif self._settings.sopa_resolution_mode == SopaResolutionMode.AVERAGE:
            for i in range(len(stabilisation_energies)):
                stabilisation_energies[i] = [mean(stabilisation_energies[i])]
        # uses the minimum and maximum values of stabilisation energies belonging to the same atom pair
        elif self._settings.sopa_resolution_mode == SopaResolutionMode.MIN_MAX:
            for i in range(len(stabilisation_energies)):
                if len(stabilisation_energies[i]) > 1:
                    stabilisation_energies[i] = [min(stabilisation_energies[i]), max(stabilisation_energies[i])]
        # uses the maximum value of stabilisation energies belonging to the same atom pair
        elif self._settings.sopa_resolution_mode == SopaResolutionMode.MAX:
            for i in range(len(stabilisation_energies)):
                stabilisation_energies[i] = [max(stabilisation_energies[i])]

        return stabilisation_energies
