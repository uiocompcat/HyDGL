from enum import Enum, auto


class GraphFeature(Enum):

    '''Enum class for the different graph features to be used.'''

    # number of atoms in molecule
    N_ATOMS = auto()
    # number of electrons in molecule
    N_ELECTRONS = auto()
    # molecular mass
    MOLECULAR_MASS = auto()
    # charge
    CHARGE = auto()
