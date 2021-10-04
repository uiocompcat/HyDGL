from enum import Enum, auto

class EdgeFeatures(Enum):

    '''Enum class for the different node features to be used.'''
    
    # will use the bond order of specified mode (Wiberg, NLMO)
    BOND_ORDER = auto()

    # euclidean distance between atoms
    BOND_DISTANCE = auto()

    # NBO data
    BOND_ORBITAL_DATA = auto()
    ANTIBOND_ORBITAL_DATA = auto()