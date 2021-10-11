from enum import Enum, auto


class EdgeFeature(Enum):

    '''Enum class for the different node features to be used.'''

    # will use the bond order of specified mode (Wiberg, NLMO)
    BOND_ORDER = auto()

    # euclidean distance between atoms
    BOND_DISTANCE = auto()

    # NBO data bonding
    BOND_ORBITAL_DATA_S = auto()
    BOND_ORBITAL_DATA_P = auto()
    BOND_ORBITAL_DATA_D = auto()
    BOND_ORBITAL_DATA_F = auto()

    # NBO data antibonding
    ANTIBOND_ORBITAL_DATA_S = auto()
    ANTIBOND_ORBITAL_DATA_P = auto()
    ANTIBOND_ORBITAL_DATA_D = auto()
    ANTIBOND_ORBITAL_DATA_F = auto()
