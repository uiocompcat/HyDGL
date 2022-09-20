from enum import Enum, auto


class SopaEdgeFeature(Enum):

    '''Enum class for the different SOPA edge features to be used.'''

    # Stabilisation energies

    STABILISATION_ENERGY_MAX = auto()
    STABILISATION_ENERGY_AVERAGE = auto()

    DONOR_NBO_TYPE = auto()
    DONOR_NBO_ENERGY = auto()
    DONOR_NBO_MIN_MAX_ENERGY_GAP = auto()
    DONOR_NBO_OCCUPATION = auto()
    DONOR_NBO_S_SYMMETRY = auto()
    DONOR_NBO_P_SYMMETRY = auto()
    DONOR_NBO_D_SYMMETRY = auto()
    DONOR_NBO_F_SYMMETRY = auto()

    ACCEPTOR_NBO_TYPE = auto()
    ACCEPTOR_NBO_ENERGY = auto()
    ACCEPTOR_NBO_MIN_MAX_ENERGY_GAP = auto()
    ACCEPTOR_NBO_OCCUPATION = auto()
    ACCEPTOR_NBO_S_SYMMETRY = auto()
    ACCEPTOR_NBO_P_SYMMETRY = auto()
    ACCEPTOR_NBO_D_SYMMETRY = auto()
    ACCEPTOR_NBO_F_SYMMETRY = auto()
