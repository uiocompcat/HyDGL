from nbo2graph.nbo_data_point import NboDataPoint


class NboDoubleDataPoint(NboDataPoint):

    """Class for storing double NBO data entries."""

    def __init__(self, nbo_id, nbo_type, atom_indices, contributions, energy, occupation, orbital_occupations):

        """Constructor"""

        super().__init__(nbo_id, nbo_type, energy, occupation, orbital_occupations)

        self._atom_indices = atom_indices
        self._contributions = contributions

    @property
    def atom_indices(self):
        """Getter for atom_indices"""
        return self._atom_indices

    @property
    def contributions(self):
        """Getter for contributions"""
        return self._contributions
