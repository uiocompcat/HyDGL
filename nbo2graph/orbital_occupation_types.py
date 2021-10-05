from enum import Enum, auto

class OrbitalOccupationTypes(Enum):

    '''Enum class for the different types of orbital occupancy in the data.'''

    LONE_PAIR = auto()
    LONE_VACANCY = auto()
    NATURAL_ELECTRON_CONFIGURATION = auto()
    BOND_ORBITAL = auto()
    ANTIBOND_ORBITAL = auto()