from .tools import Tools


class GraphElement:

    """Base class for elements of a graph."""

    def __init__(self, features: dict = {}, label: str = None, id: str = None):

        """Constructor

        Args:
            features (list[float]: List containing edge features that characterise the edge).
            label (string): Label of the graph element.
            id (string): Id of the graph element.
        """

        if type(features) == list:
            self._features = {}
            for i, feature in enumerate(features):
                self._features[str(i)] = feature
        else:
            self._features = features

        self._label = label
        self._id = id

    @property
    def features(self):
        """Getter for features"""
        return self._features

    @property
    def label(self):
        """Getter for label"""
        return self._label

    @property
    def id(self):
        """Getter for id"""
        return self._id

    @property
    def feature_list(self):
        """Getter for a list of features."""
        return [self._features[key] for key in self._features.keys()]

    def get_one_hot_encoded_feature_list(self, class_feature_dict: dict) -> list[float]:

        """Returns a feature list with class-type/string in one-hot encoding.

        Returns:
            list[float]: The feature list with one-hot encodings.
        """

        return Tools.get_one_hot_encoded_feature_list(self.features, class_feature_dict)
