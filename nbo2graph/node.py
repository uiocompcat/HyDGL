from .graph_element import GraphElement


class Node(GraphElement):

    """Class for representing a node in a graph."""

    def __init__(self, features: dict = {}, position: list[float] = None, label: str = None):

        """Constructor

        Args:
            features (list[float]: List containing node features that characterise the node).
            position (list[float]): Cartesian position of the node.
            label (string): Label of the node.
        """

        super().__init__(features)

        self._position = position
        self._label = label

    @property
    def position(self):
        """Getter for position"""
        return self._position

    @property
    def label(self):
        """Getter for label"""
        return self._label
