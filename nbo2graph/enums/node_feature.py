from enum import Enum, auto


class NodeFeature(Enum):

    '''Enum class for the different node features to be used.'''

    # basic
    ATOMIC_NUMBER = auto()
    ELECTRONEGATIVITY = auto()
    COVALENT_RADIUS = auto()

    # bound hydrogen
    BOUND_HYDROGEN_COUNT = auto()

    # bond order totals
    WIBERG_BOND_ORDER_TOTAL = auto()
    LMO_BOND_ORDER_TOTAL = auto()
    NLMO_BOND_ORDER_TOTAL = auto()

    # electron configuration
    NATURAL_ATOMIC_CHARGE = auto()

    NATURAL_ELECTRON_POPULATION_CORE = auto()
    NATURAL_ELECTRON_POPULATION_VALENCE = auto()
    NATURAL_ELECTRON_POPULATION_RYDBERG = auto()
    NATURAL_ELECTRON_POPULATION_TOTAL = auto()

    NATURAL_ELECTRON_CONFIGURATION_S_SYMMETRY = auto()
    NATURAL_ELECTRON_CONFIGURATION_P_SYMMETRY = auto()
    NATURAL_ELECTRON_CONFIGURATION_D_SYMMETRY = auto()
    NATURAL_ELECTRON_CONFIGURATION_F_SYMMETRY = auto()

    # lone pairs
    LONE_PAIR_ENERGY_MIN_MAX_DIFFERENCE = auto()

    LONE_PAIR_MAX = auto()
    LONE_PAIR_AVERAGE = auto()

    LONE_PAIR_S_SYMMETRY = auto()
    LONE_PAIR_P_SYMMETRY = auto()
    LONE_PAIR_D_SYMMETRY = auto()
    LONE_PAIR_F_SYMMETRY = auto()

    # lone vacancies
    LONE_VACANCY_ENERGY_MIN_MAX_DIFFERENCE = auto()

    LONE_VACANCY_MIN = auto()
    LONE_VACANCY_AVERAGE = auto()

    LONE_VACANCY_S_SYMMETRY = auto()
    LONE_VACANCY_P_SYMMETRY = auto()
    LONE_VACANCY_D_SYMMETRY = auto()
    LONE_VACANCY_F_SYMMETRY = auto()

    # graph
    NODE_DEGREE = auto()
