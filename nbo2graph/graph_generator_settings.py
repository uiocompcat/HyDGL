from nbo2graph.enums.qm_target import QmTarget
from nbo2graph.enums.node_feature import NodeFeature
from nbo2graph.enums.edge_feature import EdgeFeature
from nbo2graph.enums.graph_feature import GraphFeature
from nbo2graph.enums.hydrogen_mode import HydrogenMode
from nbo2graph.enums.sopa_resolution_mode import SopaResolutionMode
from nbo2graph.enums.sopa_edge_feature import SopaEdgeFeature
from nbo2graph.enums.bond_order_type import BondOrderType
from nbo2graph.enums.edge_type import EdgeType
from nbo2graph.enums.orbital_occupation_type import OrbitalOccupationType

# constants for default values
DEFAULT_BOND_ORDER_MODE = BondOrderType.WIBERG
DEFAULT_HYDROGEN_MODE = HydrogenMode.EXPLICIT
DEFAULT_BOND_THRESHOLD = 0.3
DEFAULT_HYDROGEN_COUNT_THRESHOLD = 0.5
DEFAULT_SOPA_RESOLUTION_MODE = SopaResolutionMode.AVERAGE
DEFAULT_SOPA_INTERACTION_THRESHOLD = 0
DEFAULT_SOPA_CONTRIBUTION_THRESHOLD = 0.5


class GraphGeneratorSettings:

    """Class for storing graph generator settings."""

    def __init__(self,
                 node_features: list[NodeFeature],
                 edge_features: list[EdgeFeature],
                 sopa_edge_features: list[SopaEdgeFeature],
                 graph_features: list[GraphFeature],
                 targets: list[QmTarget],
                 edge_types: list[EdgeType],
                 bond_order_mode: BondOrderType,
                 hydrogen_mode: HydrogenMode,
                 hydrogen_count_threshold: float,
                 sopa_resolution_mode: SopaResolutionMode,
                 sopa_interaction_threshold: float,
                 sopa_contribution_threshold: float,
                 bond_threshold: float,
                 bond_threshold_metal: float):

        """Constructor

        Args:
            node_features (list[NodeFeature]): List of node features to extract.
            edge_features (list[EdgeFeature]): List of edge features to extract.
            sopa_edge_features (list[EdgeFeature]): List of SOPA edge features to extract.
            graph_features (list[GraphFeature]): List of graph features to extract.
            targets (list[QmTarget]): List of targets.
            edge_types (list[EdgeType]): List of edges to include.
            bond_order_mode (BondOrderMode): Specifies which bond orders to use
            hydrogen_mode (HydrogenMode): Operation mode defining the way to handle hydrogens.
            hydrogen_count_threshold(float): Threshold value defining the lower bound for considering hydrogens as bound for implicit mode.
            sopa_resolution_mode (SopaResolutionMode): Mode that specifies how to build the SOPA edges according to the stabilisation energies.
            sopa_interaction_threshold (float): Threshold value specifying when to consider SOPA entries (in kcal/mol).
            sopa_contribution_threshold (float): Threshold value specifying when to consider atoms for NBO interactions with more than one involved atom (in %).
            bond_threshold (float): Threshold value defining the lower bound for considering bonds.
            bond_threshold_metal (float): Threshold value defining the lower bound for considering metal bonds.

        """

        # features
        self.node_features = node_features
        self.edge_features = edge_features
        self.sopa_edge_features = sopa_edge_features
        self.graph_features = graph_features

        # targets
        self.targets = targets

        # bond mode
        self.edge_types = edge_types
        self.bond_order_mode = bond_order_mode
        self.bond_threshold = bond_threshold

        if bond_threshold_metal is None:
            self.bond_threshold_metal = self.bond_threshold
        else:
            self.bond_threshold_metal = bond_threshold_metal

        # hydrogen mode
        self.hydrogen_mode = hydrogen_mode
        self.hydrogen_count_threshold = hydrogen_count_threshold

        # SOPA settings
        self.sopa_resolution_mode = sopa_resolution_mode
        self.sopa_interaction_threshold = sopa_interaction_threshold
        self.sopa_contribution_threshold = sopa_contribution_threshold

        # get orbital lists specifying which orbitals to consider
        # 0 -> s, 1 -> p, 2 -> d, 3 -> f
        self.lone_pair_orbital_indices = self._get_orbtials_to_extract_indices(OrbitalOccupationType.LONE_PAIR)
        self.lone_vacancy_orbital_indices = self._get_orbtials_to_extract_indices(OrbitalOccupationType.LONE_VACANCY)
        self.natural_orbital_configuration_indices = self._get_orbtials_to_extract_indices(OrbitalOccupationType.NATURAL_ELECTRON_CONFIGURATION)
        self.bond_orbital_indices = self._get_orbtials_to_extract_indices(OrbitalOccupationType.BOND_ORBITAL)
        self.antibond_orbital_indices = self._get_orbtials_to_extract_indices(OrbitalOccupationType.ANTIBOND_ORBITAL)

    def __eq__(self, other):

        """Equality interface that allows comparison between objects for unit testing"""

        return self.node_features == other.node_features and \
            self.edge_features == other.edge_features and \
            self.graph_features == other.graph_features and \
            self.targets == other.targets and \
            self.bond_order_mode == other.bond_order_mode and \
            self.bond_threshold == other.bond_threshold and \
            self.bond_threshold_metal == other.bond_threshold_metal and \
            self.hydrogen_mode == other.hydrogen_mode and \
            self.hydrogen_count_threshold == other.hydrogen_count_threshold and \
            self.lone_pair_orbital_indices == other.lone_pair_orbital_indices and \
            self.lone_vacancy_orbital_indices == other.lone_vacancy_orbital_indices and \
            self.natural_orbital_configuration_indices == other.natural_orbital_configuration_indices and \
            self.bond_orbital_indices == other.bond_orbital_indices and \
            self.antibond_orbital_indices == other.antibond_orbital_indices and \
            self.sopa_resolution_mode == other.sopa_resolution_mode and \
            self.sopa_contribution_threshold == other.sopa_contribution_threshold and \
            self.sopa_edge_features == other.sopa_edge_features

    @classmethod
    def default(cls,
                node_features: list[NodeFeature] = [],
                edge_features: list[EdgeFeature] = [],
                sopa_edge_features: list[SopaEdgeFeature] = [],
                graph_features: list[GraphFeature] = [],
                targets: list[QmTarget] = [],
                edge_types: list[EdgeType] = [],
                bond_order_mode: BondOrderType = DEFAULT_BOND_ORDER_MODE,
                bond_threshold: float = DEFAULT_BOND_THRESHOLD,
                bond_threshold_metal: float = None,
                hydrogen_mode: HydrogenMode = DEFAULT_HYDROGEN_MODE,
                hydrogen_count_threshold: float = DEFAULT_HYDROGEN_COUNT_THRESHOLD,
                sopa_resolution_mode: SopaResolutionMode = DEFAULT_SOPA_RESOLUTION_MODE,
                sopa_interaction_threshold: float = DEFAULT_SOPA_INTERACTION_THRESHOLD,
                sopa_contribution_threshold: float = DEFAULT_SOPA_CONTRIBUTION_THRESHOLD):

        return cls(node_features=node_features,
                   edge_features=edge_features,
                   sopa_edge_features=sopa_edge_features,
                   graph_features=graph_features,
                   targets=targets,
                   edge_types=edge_types,
                   bond_order_mode=bond_order_mode,
                   bond_threshold=bond_threshold,
                   bond_threshold_metal=bond_threshold_metal,
                   hydrogen_mode=hydrogen_mode,
                   hydrogen_count_threshold=hydrogen_count_threshold,
                   sopa_resolution_mode=sopa_resolution_mode,
                   sopa_interaction_threshold=sopa_interaction_threshold,
                   sopa_contribution_threshold=sopa_contribution_threshold)

    def _get_orbtials_to_extract_indices(self, mode: OrbitalOccupationType):

        """Helper function to parse information about which orbitals occupancies to use as node/edge features.

        Returns:
            list[int]: List specifying which orbital occupancies to consider (0 -> s, 1 -> p, 2 -> d, 3 -> f).
        """

        orbital_indices = []

        if mode == OrbitalOccupationType.LONE_PAIR:
            if NodeFeature.LONE_PAIRS_S in self.node_features:
                orbital_indices.append(0)
            if NodeFeature.LONE_PAIRS_P in self.node_features:
                orbital_indices.append(1)
            if NodeFeature.LONE_PAIRS_D in self.node_features:
                orbital_indices.append(2)
            if NodeFeature.LONE_PAIRS_F in self.node_features:
                orbital_indices.append(3)
        elif mode == OrbitalOccupationType.LONE_VACANCY:
            if NodeFeature.LONE_VACANCIES_S in self.node_features:
                orbital_indices.append(0)
            if NodeFeature.LONE_VACANCIES_P in self.node_features:
                orbital_indices.append(1)
            if NodeFeature.LONE_VACANCIES_D in self.node_features:
                orbital_indices.append(2)
            if NodeFeature.LONE_VACANCIES_F in self.node_features:
                orbital_indices.append(3)
        elif mode == OrbitalOccupationType.NATURAL_ELECTRON_CONFIGURATION:
            if NodeFeature.NATURAL_ELECTRON_CONFIGURATION_S in self.node_features:
                orbital_indices.append(0)
            if NodeFeature.NATURAL_ELECTRON_CONFIGURATION_P in self.node_features:
                orbital_indices.append(1)
            if NodeFeature.NATURAL_ELECTRON_CONFIGURATION_D in self.node_features:
                orbital_indices.append(2)
            if NodeFeature.NATURAL_ELECTRON_CONFIGURATION_F in self.node_features:
                orbital_indices.append(3)
        elif mode == OrbitalOccupationType.BOND_ORBITAL:
            if EdgeFeature.BOND_ORBITAL_DATA_S in self.edge_features:
                orbital_indices.append(0)
            if EdgeFeature.BOND_ORBITAL_DATA_P in self.edge_features:
                orbital_indices.append(1)
            if EdgeFeature.BOND_ORBITAL_DATA_D in self.edge_features:
                orbital_indices.append(2)
            if EdgeFeature.BOND_ORBITAL_DATA_F in self.edge_features:
                orbital_indices.append(3)
        elif mode == OrbitalOccupationType.ANTIBOND_ORBITAL:
            if EdgeFeature.ANTIBOND_ORBITAL_DATA_S in self.edge_features:
                orbital_indices.append(0)
            if EdgeFeature.ANTIBOND_ORBITAL_DATA_P in self.edge_features:
                orbital_indices.append(1)
            if EdgeFeature.ANTIBOND_ORBITAL_DATA_D in self.edge_features:
                orbital_indices.append(2)
            if EdgeFeature.ANTIBOND_ORBITAL_DATA_F in self.edge_features:
                orbital_indices.append(3)

        return orbital_indices
