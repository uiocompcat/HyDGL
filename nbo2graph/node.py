class Node:

    """Class for representing a node in a graph."""

    def __init__(self, features: dict = {}, position: list[float] = None, label: str = None):

        """Constructor

        Args:
            features (list[float]: List containing node features that characterise the node).
            position (list[float]): Cartesian position of the node.
            label (string): Label of the node.
        """

        if type(features) == list:
            self._features = {}
            for i, feature in enumerate(features):
                self._features[str(i)] = feature
        else:
            self._features = features

        self._position = position
        self._label = label

    @property
    def features(self):
        """Getter for features"""
        return self._features

    @property
    def position(self):
        """Getter for position"""
        return self._position

    @property
    def label(self):
        """Getter for label"""
        return self._label

    @property
    def feature_list(self):
        """Getter for a list of features."""
        return [self._features[key] for key in self._features.keys()]
