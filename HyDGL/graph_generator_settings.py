from .enums.nbo_type import NboType
from .enums.qm_target import QmTarget
from .enums.node_feature import NodeFeature
from .enums.edge_feature import EdgeFeature
from .enums.graph_feature import GraphFeature
from .enums.hydrogen_mode import HydrogenMode
from .enums.sopa_resolution_mode import SopaResolutionMode
from .enums.sopa_edge_feature import SopaEdgeFeature
from .enums.bond_order_type import BondOrderType
from .enums.edge_type import EdgeType
from .enums.orbital_occupation_type import OrbitalOccupationType

# constants for default values
DEFAULT_BOND_ORDER_MODE = BondOrderType.WIBERG
DEFAULT_HYDROGEN_MODE = HydrogenMode.EXPLICIT
DEFAULT_BOND_THRESHOLD = 0.3
DEFAULT_HYDROGEN_COUNT_THRESHOLD = 0.5
DEFAULT_SOPA_RESOLUTION_MODE = SopaResolutionMode.AVERAGE
DEFAULT_SOPA_INTERACTION_THRESHOLD = 0
DEFAULT_SOPA_CONTRIBUTION_THRESHOLD = 0.5
DEFAULT_MAX_BOND_DISTANCE = 3.0


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
                 bond_threshold_metal: float,
                 max_bond_distance: float):

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
            max_bond_distance (float): The maximum bond distance allowed for considering any bonds.

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

        self.max_bond_distance = max_bond_distance

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

        self.donor_orbital_indices = self._get_orbtials_to_extract_indices(OrbitalOccupationType.DONOR)
        self.acceptor_orbital_indices = self._get_orbtials_to_extract_indices(OrbitalOccupationType.ACCEPTOR)

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
            self.sopa_edge_features == other.sopa_edge_features and \
            self.max_bond_distance == other.max_bond_distance

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
                sopa_contribution_threshold: float = DEFAULT_SOPA_CONTRIBUTION_THRESHOLD,
                max_bond_distance: float = DEFAULT_MAX_BOND_DISTANCE):

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
                   sopa_contribution_threshold=sopa_contribution_threshold,
                   max_bond_distance=max_bond_distance)

    @classmethod
    def baseline(cls, targets):

        return cls(node_features=[NodeFeature.ATOMIC_NUMBER,
                                  NodeFeature.NODE_DEGREE,
                                  NodeFeature.COVALENT_RADIUS,
                                  NodeFeature.ELECTRONEGATIVITY],
                   edge_features=[EdgeFeature.BOND_DISTANCE,
                                  EdgeFeature.WIBERG_BOND_ORDER_INT],
                   edge_types=[EdgeType.NBO_BONDING_ORBITALS, EdgeType.BOND_ORDER_METAL],
                   bond_order_mode=BondOrderType.WIBERG,
                   bond_threshold=DEFAULT_BOND_THRESHOLD,
                   bond_threshold_metal=0.05,
                   hydrogen_mode=HydrogenMode.EXPLICIT,
                   hydrogen_count_threshold=DEFAULT_HYDROGEN_COUNT_THRESHOLD,
                   sopa_edge_features=[],
                   graph_features=[GraphFeature.CHARGE, GraphFeature.MOLECULAR_MASS, GraphFeature.N_ATOMS, GraphFeature.N_ELECTRONS],
                   targets=targets,
                   sopa_resolution_mode=None,
                   sopa_interaction_threshold=None,
                   sopa_contribution_threshold=None,
                   max_bond_distance=DEFAULT_MAX_BOND_DISTANCE)

    @classmethod
    def uNatQ(cls, targets):

        return cls(node_features=[NodeFeature.ATOMIC_NUMBER,
                                  NodeFeature.NATURAL_ATOMIC_CHARGE,
                                  NodeFeature.NATURAL_ELECTRON_POPULATION_VALENCE,
                                  NodeFeature.NATURAL_ELECTRON_CONFIGURATION_S_SYMMETRY,
                                  NodeFeature.NATURAL_ELECTRON_CONFIGURATION_P_SYMMETRY,
                                  NodeFeature.NATURAL_ELECTRON_CONFIGURATION_D_SYMMETRY,
                                  NodeFeature.LONE_PAIR_MAX,
                                  NodeFeature.LONE_VACANCY_MIN,
                                  NodeFeature.LONE_PAIR_ENERGY_MIN_MAX_DIFFERENCE,
                                  NodeFeature.LONE_VACANCY_ENERGY_MIN_MAX_DIFFERENCE,
                                  NodeFeature.LONE_PAIR_S_SYMMETRY,
                                  NodeFeature.LONE_PAIR_P_SYMMETRY,
                                  NodeFeature.LONE_PAIR_D_SYMMETRY,
                                  NodeFeature.LONE_VACANCY_S_SYMMETRY,
                                  NodeFeature.LONE_VACANCY_P_SYMMETRY,
                                  NodeFeature.LONE_VACANCY_D_SYMMETRY,
                                  NodeFeature.BOUND_HYDROGEN_COUNT],
                   edge_features=[EdgeFeature.WIBERG_BOND_ORDER,
                                  EdgeFeature.BOND_DISTANCE,
                                  EdgeFeature.NBO_TYPE,
                                  EdgeFeature.BOND_ORBITAL_MAX,
                                  EdgeFeature.ANTIBOND_ORBITAL_MIN,
                                  EdgeFeature.BOND_ENERGY_MIN_MAX_DIFFERENCE,
                                  EdgeFeature.ANTIBOND_ENERGY_MIN_MAX_DIFFERENCE,
                                  EdgeFeature.BOND_ORBITAL_S_SYMMETRY,
                                  EdgeFeature.BOND_ORBITAL_P_SYMMETRY,
                                  EdgeFeature.BOND_ORBITAL_D_SYMMETRY,
                                  EdgeFeature.ANTIBOND_ORBITAL_S_SYMMETRY,
                                  EdgeFeature.ANTIBOND_ORBITAL_P_SYMMETRY,
                                  EdgeFeature.ANTIBOND_ORBITAL_D_SYMMETRY],
                   edge_types=[EdgeType.NBO_BONDING_ORBITALS, EdgeType.BOND_ORDER_METAL],
                   bond_order_mode=BondOrderType.WIBERG,
                   bond_threshold=DEFAULT_BOND_THRESHOLD,
                   bond_threshold_metal=0.05,
                   hydrogen_mode=HydrogenMode.EXPLICIT,
                   hydrogen_count_threshold=DEFAULT_HYDROGEN_COUNT_THRESHOLD,
                   sopa_edge_features=[],
                   graph_features=[GraphFeature.CHARGE, GraphFeature.MOLECULAR_MASS, GraphFeature.N_ATOMS, GraphFeature.N_ELECTRONS],
                   targets=targets,
                   sopa_resolution_mode=None,
                   sopa_interaction_threshold=None,
                   sopa_contribution_threshold=None,
                   max_bond_distance=DEFAULT_MAX_BOND_DISTANCE)

    @classmethod
    def dNatQ(cls, targets):

        return cls(node_features=[NodeFeature.ATOMIC_NUMBER,
                                  NodeFeature.NATURAL_ATOMIC_CHARGE,
                                  NodeFeature.NATURAL_ELECTRON_POPULATION_VALENCE,
                                  NodeFeature.NATURAL_ELECTRON_CONFIGURATION_S_SYMMETRY,
                                  NodeFeature.NATURAL_ELECTRON_CONFIGURATION_P_SYMMETRY,
                                  NodeFeature.NATURAL_ELECTRON_CONFIGURATION_D_SYMMETRY,
                                  NodeFeature.LONE_PAIR_MAX,
                                  NodeFeature.LONE_VACANCY_MIN,
                                  NodeFeature.LONE_PAIR_ENERGY_MIN_MAX_DIFFERENCE,
                                  NodeFeature.LONE_VACANCY_ENERGY_MIN_MAX_DIFFERENCE,
                                  NodeFeature.LONE_PAIR_S_SYMMETRY,
                                  NodeFeature.LONE_PAIR_P_SYMMETRY,
                                  NodeFeature.LONE_PAIR_D_SYMMETRY,
                                  NodeFeature.LONE_VACANCY_S_SYMMETRY,
                                  NodeFeature.LONE_VACANCY_P_SYMMETRY,
                                  NodeFeature.LONE_VACANCY_D_SYMMETRY,
                                  NodeFeature.BOUND_HYDROGEN_COUNT],
                   edge_features=[EdgeFeature.WIBERG_BOND_ORDER, EdgeFeature.BOND_DISTANCE],
                   edge_types=[EdgeType.SOPA],
                   bond_order_mode=BondOrderType.WIBERG,
                   bond_threshold=DEFAULT_BOND_THRESHOLD,
                   bond_threshold_metal=0.05,
                   hydrogen_mode=HydrogenMode.EXPLICIT,
                   hydrogen_count_threshold=DEFAULT_HYDROGEN_COUNT_THRESHOLD,
                   sopa_edge_features=[SopaEdgeFeature.DONOR_NBO_TYPE,
                                       SopaEdgeFeature.DONOR_NBO_ENERGY,
                                       SopaEdgeFeature.DONOR_NBO_MIN_MAX_ENERGY_GAP,
                                       SopaEdgeFeature.DONOR_NBO_OCCUPATION,
                                       SopaEdgeFeature.DONOR_NBO_S_SYMMETRY,
                                       SopaEdgeFeature.DONOR_NBO_P_SYMMETRY,
                                       SopaEdgeFeature.DONOR_NBO_D_SYMMETRY,
                                       SopaEdgeFeature.ACCEPTOR_NBO_TYPE,
                                       SopaEdgeFeature.ACCEPTOR_NBO_ENERGY,
                                       SopaEdgeFeature.ACCEPTOR_NBO_MIN_MAX_ENERGY_GAP,
                                       SopaEdgeFeature.ACCEPTOR_NBO_OCCUPATION,
                                       SopaEdgeFeature.ACCEPTOR_NBO_S_SYMMETRY,
                                       SopaEdgeFeature.ACCEPTOR_NBO_P_SYMMETRY,
                                       SopaEdgeFeature.ACCEPTOR_NBO_D_SYMMETRY,
                                       SopaEdgeFeature.STABILISATION_ENERGY_MAX,
                                       SopaEdgeFeature.STABILISATION_ENERGY_AVERAGE],
                   graph_features=[GraphFeature.CHARGE,
                                   GraphFeature.MOLECULAR_MASS,
                                   GraphFeature.N_ATOMS,
                                   GraphFeature.N_ELECTRONS],
                   targets=targets,
                   sopa_resolution_mode=SopaResolutionMode.MAX,
                   sopa_interaction_threshold=1,
                   sopa_contribution_threshold=0,
                   max_bond_distance=DEFAULT_MAX_BOND_DISTANCE)

    def _get_orbtials_to_extract_indices(self, mode: OrbitalOccupationType):

        """Helper function to parse information about which orbitals occupancies to use as node/edge features.

        Returns:
            list[int]: List specifying which orbital occupancies to consider (0 -> s, 1 -> p, 2 -> d, 3 -> f).
        """

        orbital_indices = []

        if mode == OrbitalOccupationType.LONE_PAIR:
            if NodeFeature.LONE_PAIR_S_SYMMETRY in self.node_features:
                orbital_indices.append(0)
            if NodeFeature.LONE_PAIR_P_SYMMETRY in self.node_features:
                orbital_indices.append(1)
            if NodeFeature.LONE_PAIR_D_SYMMETRY in self.node_features:
                orbital_indices.append(2)
            if NodeFeature.LONE_PAIR_F_SYMMETRY in self.node_features:
                orbital_indices.append(3)
        elif mode == OrbitalOccupationType.LONE_VACANCY:
            if NodeFeature.LONE_VACANCY_S_SYMMETRY in self.node_features:
                orbital_indices.append(0)
            if NodeFeature.LONE_VACANCY_P_SYMMETRY in self.node_features:
                orbital_indices.append(1)
            if NodeFeature.LONE_VACANCY_D_SYMMETRY in self.node_features:
                orbital_indices.append(2)
            if NodeFeature.LONE_VACANCY_F_SYMMETRY in self.node_features:
                orbital_indices.append(3)
        elif mode == OrbitalOccupationType.NATURAL_ELECTRON_CONFIGURATION:
            if NodeFeature.NATURAL_ELECTRON_CONFIGURATION_S_SYMMETRY in self.node_features:
                orbital_indices.append(0)
            if NodeFeature.NATURAL_ELECTRON_CONFIGURATION_P_SYMMETRY in self.node_features:
                orbital_indices.append(1)
            if NodeFeature.NATURAL_ELECTRON_CONFIGURATION_D_SYMMETRY in self.node_features:
                orbital_indices.append(2)
            if NodeFeature.NATURAL_ELECTRON_CONFIGURATION_F_SYMMETRY in self.node_features:
                orbital_indices.append(3)
        elif mode == OrbitalOccupationType.BOND_ORBITAL:
            if EdgeFeature.BOND_ORBITAL_S_SYMMETRY in self.edge_features:
                orbital_indices.append(0)
            if EdgeFeature.BOND_ORBITAL_P_SYMMETRY in self.edge_features:
                orbital_indices.append(1)
            if EdgeFeature.BOND_ORBITAL_D_SYMMETRY in self.edge_features:
                orbital_indices.append(2)
            if EdgeFeature.BOND_ORBITAL_F_SYMMETRY in self.edge_features:
                orbital_indices.append(3)
        elif mode == OrbitalOccupationType.ANTIBOND_ORBITAL:
            if EdgeFeature.ANTIBOND_ORBITAL_S_SYMMETRY in self.edge_features:
                orbital_indices.append(0)
            if EdgeFeature.ANTIBOND_ORBITAL_P_SYMMETRY in self.edge_features:
                orbital_indices.append(1)
            if EdgeFeature.ANTIBOND_ORBITAL_D_SYMMETRY in self.edge_features:
                orbital_indices.append(2)
            if EdgeFeature.ANTIBOND_ORBITAL_F_SYMMETRY in self.edge_features:
                orbital_indices.append(3)
        elif mode == OrbitalOccupationType.DONOR:
            if SopaEdgeFeature.DONOR_NBO_S_SYMMETRY in self.sopa_edge_features:
                orbital_indices.append(0)
            if SopaEdgeFeature.DONOR_NBO_P_SYMMETRY in self.sopa_edge_features:
                orbital_indices.append(1)
            if SopaEdgeFeature.DONOR_NBO_D_SYMMETRY in self.sopa_edge_features:
                orbital_indices.append(2)
            if SopaEdgeFeature.DONOR_NBO_F_SYMMETRY in self.sopa_edge_features:
                orbital_indices.append(3)
        elif mode == OrbitalOccupationType.ACCEPTOR:
            if SopaEdgeFeature.ACCEPTOR_NBO_S_SYMMETRY in self.sopa_edge_features:
                orbital_indices.append(0)
            if SopaEdgeFeature.ACCEPTOR_NBO_P_SYMMETRY in self.sopa_edge_features:
                orbital_indices.append(1)
            if SopaEdgeFeature.ACCEPTOR_NBO_D_SYMMETRY in self.sopa_edge_features:
                orbital_indices.append(2)
            if SopaEdgeFeature.ACCEPTOR_NBO_F_SYMMETRY in self.sopa_edge_features:
                orbital_indices.append(3)

        return orbital_indices

    def get_nbo_orbital_indices_by_type(self, nbo_type: NboType):

        if nbo_type == NboType.LONE_PAIR:
            return self.lone_pair_orbital_indices
        elif nbo_type == NboType.LONE_VACANCY:
            return self.lone_vacancy_orbital_indices
        elif nbo_type == NboType.BOND:
            return self.bond_orbital_indices
        elif nbo_type == NboType.ANTIBOND:
            return self.antibond_orbital_indices
        elif nbo_type == NboType.THREE_CENTER_BOND:
            return self.bond_orbital_indices
        elif nbo_type == NboType.THREE_CENTER_ANTIBOND:
            return self.antibond_orbital_indices
        elif nbo_type == NboType.THREE_CENTER_NONBOND:
            return self.antibond_orbital_indices
        else:
            raise ValueError('NboType ' + str(nbo_type) + ' not recognized.')
