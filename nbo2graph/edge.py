class Edge:

    """Class for representing an edge in a graph."""

    def __init__(self, node_indices: list[int], features: dict = {}, is_directed: bool = False):

        """Constructor

        Args:
            node_indices (list[int]): Indices of the connected nodes.
            features (list[float]: List containing edge features that characterise the edge).
            is_directed (bool): Denotes whether or not the edge is directed.
        """

        if type(features) == list:
            self._features = {}
            for i, feature in enumerate(features):
                self._features[str(i)] = feature
        else:
            self._features = features

        self._node_indices = node_indices
        self._is_directed = is_directed

    @property
    def node_indices(self):
        """Getter for node_indices"""
        return self._node_indices

    @property
    def features(self):
        """Getter for features"""
        return self._features

    @property
    def is_directed(self):
        """Getter for is_directed"""
        return self._is_directed

    @property
    def feature_list(self):
        """Getter for a list of features."""
        return [self._features[key] for key in self._features.keys()]
