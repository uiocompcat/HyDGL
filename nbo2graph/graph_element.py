class GraphElement:

    """Abstract class for elements of a graph."""

    def __init__(self, features: dict = {}):

        """Constructor

        Args:
            features (list[float]: List containing edge features that characterise the edge).
        """

        if type(features) == list:
            self._features = {}
            for i, feature in enumerate(features):
                self._features[str(i)] = feature
        else:
            self._features = features

    @property
    def features(self):
        """Getter for features"""
        return self._features

    @property
    def feature_list(self):
        """Getter for a list of features."""
        return [self._features[key] for key in self._features.keys()]
