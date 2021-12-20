from enum import Enum, auto


class BondOrderType(Enum):

    '''Enum class for the different modes of determining bonds in the molecule.'''

    # Use the Wiberg index matrix to determine bonds
    WIBERG = auto()
    # Use the Localised Molecular Orbitals (LMO) to determine bonds
    LMO = auto()
    # Use the Natural Localised Molecular Orbitals (NLMO) to determine bonds
    NLMO = auto()
