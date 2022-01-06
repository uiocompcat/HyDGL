from enum import Enum, auto


class OrbitalOccupationType(Enum):

    '''Enum class for the different types of orbital occupancy in the data.'''

    # general
    NATURAL_ELECTRON_CONFIGURATION = auto()
    LONE_PAIR = auto()
    LONE_VACANCY = auto()
    BOND_ORBITAL = auto()
    ANTIBOND_ORBITAL = auto()
