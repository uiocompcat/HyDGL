from enum import Enum, auto

class NodeFeatures(Enum):

    '''Enum class for the different node features to be used.'''
    
    # basic
    ATOMIC_NUMBERS = auto()
    NATURAL_ATOMIC_CHARGES = auto()
    NATURAL_ELECTRON_CONFIGURATION = auto()

    BOND_ORDER_TOTAL = auto()

    LONE_PAIRS = auto()
    LONE_VACANCIES = auto()