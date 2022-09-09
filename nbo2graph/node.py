from .graph_element import GraphElement


class Node(GraphElement):

    """Class for representing a node in a graph."""

    def __init__(self, features: dict = {}, position: list[float] = None, label: str = None, id: str = None):

        """Constructor

        Args:
            features (list[float]: List containing node features that characterise the node).
            position (list[float]): Cartesian position of the node.
            label (string): Label of the node.
            id (string): Id of the node.
        """

        super().__init__(features, label=label, id=id)

        self._position = position

    @property
    def position(self):
        """Getter for position"""
        return self._position
