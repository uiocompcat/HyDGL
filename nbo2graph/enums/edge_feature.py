from enum import Enum, auto


class EdgeFeature(Enum):

    '''Enum class for the different edge features to be used.'''

    # bond orders
    WIBERG_BOND_ORDER = auto()
    LMO_BOND_ORDER = auto()
    NLMO_BOND_ORDER = auto()

    # NBO type
    NBO_TYPE = auto()

    # euclidean distance between atoms
    BOND_DISTANCE = auto()

    # NBO data bonding
    BOND_ENERGY_MIN_MAX_DIFFERENCE = auto()

    BOND_ORBITAL_MAX = auto()
    BOND_ORBITAL_AVERAGE = auto()

    BOND_ORBITAL_DATA_S = auto()
    BOND_ORBITAL_DATA_P = auto()
    BOND_ORBITAL_DATA_D = auto()
    BOND_ORBITAL_DATA_F = auto()

    # NBO data antibonding
    ANTIBOND_ENERGY_MIN_MAX_DIFFERENCE = auto()

    ANTIBOND_ORBITAL_MIN = auto()
    ANTIBOND_ORBITAL_AVERAGE = auto()

    ANTIBOND_ORBITAL_DATA_S = auto()
    ANTIBOND_ORBITAL_DATA_P = auto()
    ANTIBOND_ORBITAL_DATA_D = auto()
    ANTIBOND_ORBITAL_DATA_F = auto()
