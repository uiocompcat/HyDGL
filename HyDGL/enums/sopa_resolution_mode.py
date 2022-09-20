from enum import Enum, auto


class SopaResolutionMode(Enum):

    '''Enum class for the different ways of resolving multiple SOPA entries of the same atoms.'''

    FULL = auto()
    MAX = auto()
    MIN = auto()
    MIN_MAX = auto()
    AVERAGE = auto()
