from enum import Enum, auto


class EdgeFeature(Enum):

    '''Enum class for the different edge features to be used.'''

    # bond orders
    WIBERG_BOND_ORDER = auto()
    LMO_BOND_ORDER = auto()
    NLMO_BOND_ORDER = auto()

    # integer bond orders
    # LMO and NLMO bond orders can be negative so that there is no clear conversion
    # to integer bond orders
    WIBERG_BOND_ORDER_INT = auto()

    # NBO type
    NBO_TYPE = auto()

    # euclidean distance between atoms
    BOND_DISTANCE = auto()

    # NBO data bonding
    BOND_ENERGY_MIN_MAX_DIFFERENCE = auto()

    BOND_ORBITAL_MAX = auto()
    BOND_ORBITAL_AVERAGE = auto()

    BOND_ORBITAL_S_SYMMETRY = auto()
    BOND_ORBITAL_P_SYMMETRY = auto()
    BOND_ORBITAL_D_SYMMETRY = auto()
    BOND_ORBITAL_F_SYMMETRY = auto()

    # NBO data antibonding
    ANTIBOND_ENERGY_MIN_MAX_DIFFERENCE = auto()

    ANTIBOND_ORBITAL_MIN = auto()
    ANTIBOND_ORBITAL_AVERAGE = auto()

    ANTIBOND_ORBITAL_S_SYMMETRY = auto()
    ANTIBOND_ORBITAL_P_SYMMETRY = auto()
    ANTIBOND_ORBITAL_D_SYMMETRY = auto()
    ANTIBOND_ORBITAL_F_SYMMETRY = auto()
