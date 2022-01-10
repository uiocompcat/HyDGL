from enum import Enum, auto


class SopaEdgeFeature(Enum):

    '''Enum class for the different SOPA edge features to be used.'''

    # Stabilisation energies

    STABILISATION_ENERGY_MAX = auto()
    STABILISATION_ENERGY_AVERAGE = auto()

    ACCEPTOR_NBO_TYPE = auto()
    DONOR_NBO_TYPE = auto()
