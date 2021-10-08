from enum import Enum, auto

class GraphFeature(Enum):

    '''Enum class for the different graph features to be used.'''
    
    # number of atoms in molcule
    N_ATOMS = auto()
    # molecular mass
    MOLECULAR_MASS = auto()
    # charge 
    CHARGE = auto()
    # POLARISABILITY
    POLARISABILITY = auto()

    # csd code
    CSD_CODE = auto()
    # STOICHIOMETRY
    STOICHIOMETRY = auto()