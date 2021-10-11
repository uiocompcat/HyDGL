from enum import Enum, auto


class HydrogenMode(Enum):

    '''Enum class for the different ways to handle hydrogens in the molecule graph.'''

    # hydrogens are explicitly included in the graph as nodes
    EXPLICIT = auto()
    # hydrogens are ignored and not included in the graph
    OMIT = auto()
    # hydrogens are not included as nodes, but all heavy atom nodes receive
    # an additional feature that display the number of bound hydrogens
    IMPLICIT = auto()
