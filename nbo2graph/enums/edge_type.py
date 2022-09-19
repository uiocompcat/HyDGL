from enum import Enum, auto


class EdgeType(Enum):

    '''Enum class for the different types of edges.'''

    # use bonds as calculated from nbo analysis
    NBO_BONDING_ORBITALS = auto()

    BOND_ORDER_NON_METAL = auto()
    BOND_ORDER_METAL = auto()

    SOPA = auto()
    SOPA_NBO = auto()
