from enum import Enum, auto


class NodeFeature(Enum):

    '''Enum class for the different node features to be used.'''

    # basic
    ATOMIC_NUMBERS = auto()

    WIBERG_BOND_ORDER_TOTAL = auto()
    LMO_BOND_ORDER_TOTAL = auto()
    NLMO_BOND_ORDER_TOTAL = auto()

    # electron configuration
    NATURAL_ATOMIC_CHARGES = auto()

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

    LONE_PAIRS_S = auto()
    LONE_PAIRS_P = auto()
    LONE_PAIRS_D = auto()
    LONE_PAIRS_F = auto()

    # lone vacancies
    LONE_VACANCY_ENERGY_MIN_MAX_DIFFERENCE = auto()

    LONE_VACANCY_MIN = auto()
    LONE_VACANCY_AVERAGE = auto()

    LONE_VACANCIES_S = auto()
    LONE_VACANCIES_P = auto()
    LONE_VACANCIES_D = auto()
    LONE_VACANCIES_F = auto()
