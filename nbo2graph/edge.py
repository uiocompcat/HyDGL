from .graph_element import GraphElement


class Edge(GraphElement):

    """Class for representing an edge in a graph."""

    def __init__(self, node_indices: list[int], features: dict = {}, is_directed: bool = False):

        """Constructor

        Args:
            node_indices (list[int]): Indices of the connected nodes.
            features (list[float]: List containing edge features that characterise the edge).
            is_directed (bool): Denotes whether or not the edge is directed.
        """

        super().__init__(features)

        self._node_indices = node_indices
        self._is_directed = is_directed

    @property
    def node_indices(self):
        """Getter for node_indices"""
        return self._node_indices

    @property
    def is_directed(self):
        """Getter for is_directed"""
        return self._is_directed
