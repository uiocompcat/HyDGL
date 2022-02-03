from enum import Enum, auto


class NodeFeature(Enum):

    '''Enum class for the different node features to be used.'''

    # basic
    ATOMIC_NUMBER = auto()

    BOUND_HYDROGEN_COUNT = auto()

    WIBERG_BOND_ORDER_TOTAL = auto()
    LMO_BOND_ORDER_TOTAL = auto()
    NLMO_BOND_ORDER_TOTAL = auto()

    # electron configuration
    NATURAL_ATOMIC_CHARGE = auto()

    NATURAL_ELECTRON_POPULATION_CORE = auto()
    NATURAL_ELECTRON_POPULATION_VALENCE = auto()
    NATURAL_ELECTRON_POPULATION_RYDBERG = auto()
    NATURAL_ELECTRON_POPULATION_TOTAL = auto()

    NATURAL_ELECTRON_CONFIGURATION_S = auto()
    NATURAL_ELECTRON_CONFIGURATION_P = auto()
    NATURAL_ELECTRON_CONFIGURATION_D = auto()
    NATURAL_ELECTRON_CONFIGURATION_F = auto()

    # lone pairs
    LONE_PAIR_ENERGY_MIN_MAX_DIFFERENCE = auto()

    LONE_PAIR_MAX = auto()
    LONE_PAIR_AVERAGE = auto()

    LONE_PAIR_S = auto()
    LONE_PAIR_P = auto()
    LONE_PAIR_D = auto()
    LONE_PAIR_F = auto()

    # lone vacancies
    LONE_VACANCY_ENERGY_MIN_MAX_DIFFERENCE = auto()

    LONE_VACANCY_MIN = auto()
    LONE_VACANCY_AVERAGE = auto()

    LONE_VACANCY_S = auto()
    LONE_VACANCY_P = auto()
    LONE_VACANCY_D = auto()
    LONE_VACANCY_F = auto()
