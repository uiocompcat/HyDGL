from enum import Enum, auto


class NboType(Enum):

    '''Enum class for the different NBO types to be used.'''

    BOND = auto()
    ANTIBOND = auto()
    LONE_VACANCY = auto()
    LONE_PAIR = auto()
    THREE_CENTER_BOND = auto()
    THREE_CENTER_ANTIBOND = auto()
    THREE_CENTER_NONBOND = auto()
